import ubinascii

print('[main]')
print('Welcome to the TitlESP32!')
 
if not wlan.isconnected():
    print('Wifi not connected')
else:
    print('ip :', ip)
    print('netmask:', netmask)
    print('gateway:', gateway)
    print('DNS :', dns)
    print('MAC :', ubinascii.hexlify(wlan.config('mac'),':').decode('utf-8'))