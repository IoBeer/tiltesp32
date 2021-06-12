from time import sleep, time
from struct import unpack
import ubinascii
import _thread
import webserver
import ubluetooth
from micropython import const
import gc
import ujson
import urequests

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

#Tilt format based on iBeacon format and filter includes Apple iBeacon identifier portion (4c000215) as well as Tilt specific uuid preamble (a495)
TILT = '4c000215a495'

print('[main]')
print('Welcome to the TitlESP32!')
 
if not wlan.isconnected():
    print('Wifi not connected')
else:
    print('ip :', _IP)
    print('netmask:', _NETMASK)
    print('gateway:', _GATEWAY)
    print('DNS :', _DNS)
    print('MAC :', ubinascii.hexlify(wlan.config('mac'),':').decode('utf-8'))

# Starting the webserver
# server_thread = _thread.start_new_thread(webserver.start_webserver, ())

def get_device_color(uuid):
    return list(DEVICE_COLORS.keys())[list(DEVICE_COLORS.values()).index(uuid)]

def parse_device_uuid(adv_data):
    uuid = ubinascii.hexlify(adv_data)[18:50]
    return uuid.decode('utf-8')

def handle_ibeacon(beacon_data):
    addr_type, addr, adv_type, rssi, adv_data = beacon_data
    identifier = ubinascii.hexlify(adv_data)[10:22]
    if identifier.decode("utf-8") == TILT:
        uuid = parse_device_uuid(adv_data)
        if uuid.lower() in DEVICE_COLORS.values():
            log_data(addr, adv_data)
        else:
            print("Device {} found but not match any known Tilt color".format(uuid))

def log_data(addr, payload):    
    uuid = parse_device_uuid(payload)
    mac_addr = ubinascii.hexlify(addr).decode('utf-8')
    device_color = get_device_color(uuid)
    gc.collect()

    # Search for mac address first, in case there are multiple devices with the same color
    device = None
    try:
        device = next((i for i in CONFIG['devices'] if i['mac_addr'] == mac_addr))
    except StopIteration:
        try:
            # Getting the very first device with the same color as read
            device = next((i for i in CONFIG['devices'] if i['color'].upper() == device_color))
        except StopIteration:
            print('Device {} - ({}) found but not listed in config.json'.format(uuid, device_color))
            return
        finally:
            gc.collect()

    # Get fermentation data
    temp_f = int(ubinascii.hexlify(payload)[50:54].decode('utf-8'), 16)
    sg_read = int(ubinascii.hexlify(payload)[54:58].decode('utf-8'), 16)
    gc.collect()

    # Create request data
    # request_data = ujson.dumps({ 
    #     "parameter": {
    #         "Beer": device['beer'],
    #         "Temp": temp_f,
    #         "SG":sg_read,
    #         "Color": device['color'].upper(),
    #         "Comment": '{},TiltESP32'.format(device['email']),
    #         "Timepoint": round(time() * 1000)
    #     }
    # })

    request_data = ujson.dumps({
        "message": {
            "Beer": "Coaiada Fail",
            "Temp": 65,
            "SG":1.050,
            "Color":"ORANGE",
            "Comment":"netomarin@gmail.com, TiltESP32",
            "Timepoint":43486.6
        }
    })

    gc.collect()
    print("url: {} - data: {}".format(device['cloud_url'], request_data))
    # response = urequests.post(device['cloud_url'], headers = {'content-type': 'application/json'}, data = request_data)
    response = urequests.post('https://southamerica-east1-tiltesp32.cloudfunctions.net/beerdata', headers = {'content-type': 'application/json'}, data = request_data)
    print("Response: {}".format(response))
    gc.collect()
    

def bt_irq(event, data):
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        handle_ibeacon(data)
    elif event == _IRQ_SCAN_DONE:
        # Scan duration finished or manually stopped.
        pass
    gc.collect()

# Starting BLE scan
ble = ubluetooth.BLE()
ble.active(True)
ble.irq(bt_irq)
ble.gap_scan(0,10000000,10000000)