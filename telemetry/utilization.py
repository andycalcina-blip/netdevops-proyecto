import time
from telemetry import cisco, fortigate

_prev = {}

def pct(delta_bytes, dt, speed_bps):
    if not speed_bps or dt <= 0:
        return 0.0
    return round(delta_bytes * 8 / (dt * speed_bps) * 100, 2)

def _calc(key, total, speed, now):
    prev = _prev.get(key)
    _prev[key] = (total, now)
    if prev is None:
        return 0.0
    delta = total - prev[0]
    if delta < 0:
        return 0.0
    return pct(delta, now - prev[1], speed)

def sample():
    now = time.time()
    rows = []
    for name, c in cisco.get_counters().items():
        if c['oper'] != 'up':
            continue
        u = _calc('sw:' + name, c['in'] + c['out'], c['speed_bps'], now)
        rows.append({'device': 'switch', 'interface': name, 'util_pct': u, 'status': c['oper']})
    w = fortigate.get_wan1()
    u = _calc('fgt:wan1', w['rx'] + w['tx'], w['speed_bps'], now)
    rows.append({'device': 'fortigate', 'interface': 'wan1', 'util_pct': u,
                 'status': 'up' if w['link'] else 'down'})
    return rows
