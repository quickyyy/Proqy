from modules.log import log


def remove_duplicate_proxies(proxies):
    # log.info('Starting to remove duplicate proxies')
    log.log('INFO', f'Got {len(proxies)} proxies', module='_formatter_')
    unique_proxies = []
    seen = set()
    for proxy in proxies:
        if proxy not in seen:
            unique_proxies.append(proxy)
            seen.add(proxy)
    log.log('INFO',
            f'Done. Removed proxies: {len(proxies) - len(unique_proxies)}. Got {len(unique_proxies)} unique proxy.',
            module='_formatter_')
    return unique_proxies
