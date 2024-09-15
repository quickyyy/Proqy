import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from modules.log import log
import modules.configworker as cfgworker
import modules.formatter as formatter

valid = 0
nonvalid = 0
allproxy = 0
workers = 5
checked_proxies = 0  # Add this to track checked proxies


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
        approx_time = (proxylen / workers) * 5 * len(PROXY_TYPES)
        approx_time_min = approx_time / 60
        log.info(f"Estimated time for proxy check: {approx_time_min:.1f} min ({approx_time:.0f} seconds)", module='_calctime_')
    else:
        log.error("Invalid number of proxies or workers.", module='_calctime_')

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
    global valid, nonvalid, checked_proxies
    for proxy_type in PROXY_TYPES:
        proxies = parse_proxy(proxy, proxy_type)

        try:
            response = requests.get(config['url'], proxies=proxies, timeout=int(config['response_timeout']))
            if response.status_code == 200:
                log.info(f'{proxy} works as {proxy_type} | Remains: {allproxy - checked_proxies}', module='Proqy')
                save_valid(proxy, proxy_type)
                valid += 1
                checked_proxies += 1  # Increment checked proxies
                return f"{proxy} is working as {proxy_type}."
            else:
                if config['print_invalid']:
                    log.error(f'{proxy} does not work as {proxy_type} | Remains: {allproxy - checked_proxies}', module='Proqy')
        except Exception as e:
            if config['print_invalid']:
                log.error(f'Error checking {proxy}/{proxy_type} | Remains: {allproxy - checked_proxies}', module='Proqy')

    nonvalid += 1
    checked_proxies += 1  # Increment checked proxies even for non-valid proxies
    #proxies_left = allproxy - checked_proxies
    #log.info(f"{proxies_left} proxies left to check.")

    return f"{proxy} is not valid for any proxy type."

def check_proxies_threaded(proxies):
    with ThreadPoolExecutor(max_workers=int(config['threads'])) as executor:
        results = list(executor.map(check_proxy, proxies))
    return results

def main(proxy_file):
    log.debug('Initialization...')
    global allproxy, nonvalid, valid
    proxies = load_proxies(proxy_file)
    log.info(f'Loaded {len(proxies)} proxies', module='Parser')
    proxies = formatter.remove_duplicate_proxies(proxies)
    calc_estimate_time(len(proxies), int(config['threads']))
    start_time = time.time()
    #log.debug(f'Starting work in {start_time}', module='debugtime')
    check_proxies_threaded(proxies)
    end_time = time.time()
    total_time = end_time - start_time
    log.debug(f'All proxies checked in {total_time:.0f} seconds.', module='debugtime')
    print_end(valid, nonvalid)
    log.debug(f'Valid: {valid} | Nonvalid: {nonvalid} | Total: {allproxy} / Pinging site: {config["url"]}', module='Proqy')


if __name__ == "__main__":
    os.system('cls')
    log.info('Welcome to Proqy')
    log.info('You can find me here - https://github.com/quickyyy/Proqy | Or here - t.me/bredcookie')
    os.system('title "Proqy - proxy checker by @bredcookie')
    if os.path.exists('config.k3'):
        config = cfgworker.cfgread()
        config = cfgworker.checksettings(config)
        if bool(config['bruteforce_type']):
            PROXY_TYPES = ['http', 'socks4', 'socks5']
        else:
            PROXY_TYPES = [config['proxy_type']]
        main(config['proxy_file'])
        log.info('All proxies checked! Have a nice day!')
        sys.exit(0)
