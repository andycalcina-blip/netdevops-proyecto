import os, time, requests
from dotenv import load_dotenv
load_dotenv()
requests.packages.urllib3.disable_warnings()

MOCK = os.getenv('USE_MOCK') == '1'
H = {'Authorization': 'Bearer ' + str(os.getenv('FGT_KEY'))}
BASE = 'https://' + str(os.getenv('FGT_IP')) + '/api/v2/monitor/system/'

def get_status():
    if MOCK:
        return {'hostname': 'FGT-MOCK', 'version': 'v7.4.1'}
    r = requests.get(BASE + 'status', headers=H, verify=False, timeout=10)
    r.raise_for_status()
    return r.json()

def get_wan1():
    if MOCK:
        t = time.time()
        return {'ip': '172.23.18.225', 'mask': '255.255.255.0', 'link': True,
                'speed_bps': 1000000000, 'rx': int(t * 500000), 'tx': int(t * 250000)}
    r = requests.get(BASE + 'interface', params={'interface_name': 'wan1'}, headers=H, verify=False, timeout=10)
    r.raise_for_status()
    w = r.json()['results']['wan1']
    return {'ip': w.get('ip'), 'mask': w.get('mask'), 'link': w.get('link'),
            'speed_bps': int(float(w.get('speed', 0)) * 1000000),
            'rx': int(w.get('rx_bytes', 0)), 'tx': int(w.get('tx_bytes', 0))}
