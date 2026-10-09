import os, time, requests
from dotenv import load_dotenv

load_dotenv()

MOCK = os.getenv('USE_MOCK') == '1'
KEY = str(os.getenv('FGT_KEY'))
IP = str(os.getenv('FGT_IP'))

H = {'Authorization': f'Bearer {KEY}'}
BASE = f'http://{IP}/api/v2/monitor/system/'

def get_status():
    if MOCK:
        return {'hostname': 'FGT-MOCK', 'version': 'v7.4.1'}
    
    r = requests.get(BASE + 'status', params={'vdom': 'root'}, headers=H, timeout=10)
    r.raise_for_status()
    return r.json()

def get_wan1():
    if MOCK:
        t = time.time()
        return {'ip': '192.168.81.137', 'mask': '255.255.255.0', 'link': True,
                'speed_bps': 1_000_000_000, 'rx': int(t * 500_000), 'tx': int(t * 250_000)}
    
    r = requests.get(BASE + 'interface', params={'interface_name': 'port1', 'vdom': 'root'}, headers=H, timeout=10)
    r.raise_for_status()
    w = r.json()['results']['port1']
    return {'ip': w.get('ip'), 'mask': w.get('mask'), 'link': w.get('link'),
            'speed_bps': int(float(w.get('speed', 0)) * 1_000_000),
            'rx': int(w.get('rx_bytes', 0)), 'tx': int(w.get('tx_bytes', 0))}
