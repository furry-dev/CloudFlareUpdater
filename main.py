import json
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

cf = CloudFlare(email, token=token)

while True:
    old_ip = None
    current_ip = get_external_ip()
    print(current_ip)
    if current_ip != old_ip:
        for zone in config['zones']:
            for domain in zone['domains']:
                zone_name = zone['name']

                zone = cf.zones.get(params={"name": zone_name})[0]
                record = cf.zones.dns_records.get(zone['id'], params={"name": domain, "type": "A"})[0]

                update_dns_record_ip(cf, zone['id'], record, current_ip)

                print(f'DNS запись обновлена для {domain} с IP {current_ip}')
                old_ip = current_ip
    else:
        print('IP не изменился, ожидание следующей проверки...')
    sleep(config['refresh_interval'])
