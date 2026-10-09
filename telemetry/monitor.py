import os, time
from telemetry import cisco, utilization

INTERVALO = 3
info = cisco.get_info()
utilization.sample()
time.sleep(INTERVALO)
while True:
    rows = utilization.sample()
    os.system('clear')
    print('Switch:', info['hostname'], '| IOS-XE', info['version'], '| uptime', info['uptime'])
    print('%-10s %-26s %-8s %8s' % ('DISP', 'INTERFAZ', 'ESTADO', 'USO %'))
    for r in rows:
        print('%-10s %-26s %-8s %8.2f' % (r['device'], r['interface'], r['status'], r['util_pct']))
    time.sleep(INTERVALO)
