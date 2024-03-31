import json
import logging
import sys

import requests
from time import sleep
from CloudFlare import CloudFlare


def load_config():
    with open('config.json') as f:
        return json.load(f)


def get_external_ip():
    return requests.get('https://api.ipify.org').text


def update_dns_record_ip(cf, zone_id, record, new_ip):
    record['content'] = new_ip
    cf.zones.dns_records.put(zone_id, record['id'], data=record)


config = load_config()
email = config['email']
token = config['token_key']

logger = logging.getLogger('updater')

if 'log_file_name' in config:
    log_file_name = config['log_file_name']
    logging.basicConfig(filename=log_file_name,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
else:
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

print("Running CloudFlare Updater")
logger.info("Running CloudFlare Updater")

cf = CloudFlare(email, token=token)

old_ip = None

while True:
    current_ip = get_external_ip()
    logger.info(f"Current IP: {current_ip}")
    if current_ip != old_ip:
        for zone in config['zones']:
            for domain in zone['domains']:
                zone_name = zone['name']

                zones = cf.zones.get(params={"name": zone_name})
                if len(zones) < 1:
                    logger.error(f"No records found for zone: {zone_name}")
                    continue

                records = cf.zones.dns_records.get(zones[0]['id'], params={"name": domain, "type": "A"})
                if len(records) < 1:
                    logger.error(f"No records found for domain: {domain}")
                    continue

                update_dns_record_ip(cf, zones[0]['id'], records[0], current_ip)

                logger.info(f'DNS запись обновлена для {domain} с IP {current_ip}')
        old_ip = current_ip
    else:
        logger.info('IP не изменился, ожидание следующей проверки...')
    sleep(config['refresh_interval'])
