import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from modules.log import log

valid = 0
nonvalid = 0
allproxy = 0
workers = 5

PROXY_TYPES = ['http', 'socks4', 'socks5']


def print_end(goodp, baadp):
    allproxy = goodp + baadp
    print(f"""
            Вся работа окончена!
  Проверено прокси   Валидных   Не работают  
 ------------------ ---------- ------------- 
         {allproxy}              {goodp}            {baadp}               

    """)

def calc_estimate_time(proxylen, workers):
    if proxylen > 0 and workers > 0:
        approx_time = (allproxy / workers) * 5 * len(PROXY_TYPES)
        approx_time_min = approx_time / 60
        log.info(f"Estimated time for proxy check: {approx_time_min:.1f} min ({approx_time:.0f} seconds)")
    else:
        log.error("Invalid number of proxies or workers.")
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        global allproxy
        allproxy = len(lines)
        proxies = [line.strip() for line in lines]
        return proxies


def save_valid(proxy, proxy_type):
    file_path = f'valid_proxies_{proxy_type}.txt'
    with open(file_path, 'a') as file:
        file.write(f"{proxy}\n")


def parse_proxy(proxy, proxy_type):
    if '@' in proxy:
        proxy_address, creds = proxy.split('@')
        username, password = creds.split(':')
        return {
            "http": f'{proxy_type}://{username}:{password}@{proxy_address}',
            "https": f'{proxy_type}://{username}:{password}@{proxy_address}',
        }
    else:
        return {
            "http": f'{proxy_type}://{proxy}',
            "https": f'{proxy_type}://{proxy}',
        }


def check_proxy(proxy):
    global valid, nonvalid

    for proxy_type in PROXY_TYPES:
        proxies = parse_proxy(proxy, proxy_type)
        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                log.info(f'{proxy} works as {proxy_type}')
                save_valid(proxy, proxy_type)
                valid += 1
                return f"{proxy} is working as {proxy_type}."
            else:
                if not printinvalid:
                    log.error(f'{proxy} does not work as {proxy_type}')
        except Exception as e:
            if not printinvalid:
                log.error(f'{proxy}/{proxy_type}')

    nonvalid += 1
    return f"{proxy} is not valid for any proxy type."


def check_proxies_threaded(proxies):
    log.info('Starting checking proxies')
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(check_proxy, proxies))
    return results


def main(proxy_file):
    log.debug('Initialization...')
    global allproxy, nonvalid, valid
    proxies = load_proxies(proxy_file)
    log.info(f'Loaded {len(proxies)} proxies')
    calc_estimate_time(len(proxies), workers)
    start_time = time.time()
    log.debug(f'Starting work in {start_time}')
    check_proxies_threaded(proxies)
    end_time = time.time()
    total_time = end_time - start_time
    log.debug(f'All proxies checked in {total_time:.0f} seconds.')
    print_end(valid, nonvalid)
    log.debug(f'Valid: {valid} | Nonvalid: {nonvalid} | Total: {allproxy} / Pinging site: {test_url}')


if __name__ == "__main__":
    os.system('cls')
    log.info('Welcome to Proqy')
    log.info('You can find me here - https://github.com/quickyyy/Proqy | Or here - @bredcookie')
    os.system('title "Proqy - proxy checker by @bredcookie')
    test_url = log.input('Which site going to test? (Default: https://httpbin.org): ')
    if test_url == '':
        log.debug('The site being tested is not specified. Will use httpbin.org')
        test_url = 'https://httpbin.org/ip'
    workers = int(log.input('How many workers do you want to use? (Default: 15): '))
    if workers == '':
        workers = 15
    printinvalid = bool(log.input('Do you want to print invalid proxies? (True/False) (Default: True): '))
    if printinvalid == '':
        printinvalid = True
    proxy_file = log.input('Enter path to proxy file (Default: proxies.txt): ')
    proxy_type = log.input('You know what type of proxy you would like to check? (https/socks4/socks5) (leave blank clear for check all types): ').lower()
    if proxy_type != '':
        PROXY_TYPES = [proxy_type]
    main(proxy_file)
