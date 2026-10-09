import os, time, requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
requests.packages.urllib3.disable_warnings()

MOCK = os.getenv('USE_MOCK') == '1'
IP = os.getenv('SW1_IP')
AUTH = (os.getenv('SW_USER'), os.getenv('SW_PASS'))
H = {'Accept': 'application/yang-data+json'}

def _get(path):
    url = 'https://' + str(IP) + '/restconf/data/' + path
    r = requests.get(url, auth=AUTH, headers=H, verify=False, timeout=10)
    r.raise_for_status()
    return r.json()

def get_uptime():
    try:
        p = 'Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-hardware/device-system-data'
        s = _get(p)['Cisco-IOS-XE-device-hardware-oper:device-system-data']
        t0 = datetime.fromisoformat(s['boot-time'])
        t1 = datetime.fromisoformat(s['current-time'])
        return str(t1 - t0)
    except Exception:
        return 'n/d'

def get_info():
    if MOCK:
        return {'hostname': 'SW-MOCK', 'version': '17.9.4', 'uptime': '3 days, 4:10:00'}
    n = _get('Cisco-IOS-XE-native:native')['Cisco-IOS-XE-native:native']
    return {'hostname': n['hostname'], 'version': n['version'], 'uptime': get_uptime()}

def get_counters():
    if MOCK:
        t = time.time()
        return {
            'GigabitEthernet1/0/1': {'oper': 'up', 'speed_bps': 1000000000, 'in': int(t * 2000000), 'out': int(t * 1000000)},
            'GigabitEthernet1/0/2': {'oper': 'up', 'speed_bps': 100000000, 'in': int(t * 3000000), 'out': int(t * 1500000)},
            'GigabitEthernet1/0/3': {'oper': 'down', 'speed_bps': 1000000000, 'in': 0, 'out': 0}}
    out = {}
    data = _get('ietf-interfaces:interfaces-state')
    for i in data['ietf-interfaces:interfaces-state']['interface']:
        out[i['name']] = {
            'oper': i['oper-status'],
            'speed_bps': int(i.get('speed', 0)),
            'in': int(i['statistics']['in-octets']),
            'out': int(i['statistics']['out-octets'])}
    return out
