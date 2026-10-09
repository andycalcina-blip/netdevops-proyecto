from telemetry import cisco, fortigate
print('SWITCH   :', cisco.get_info())
print('FORTIGATE:', fortigate.get_status())
print('WAN1     :', fortigate.get_wan1())
