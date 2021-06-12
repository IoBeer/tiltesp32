import ujson
import network
import gc
import esp

esp.osdebug(None)
wlan = network.WLAN(network.STA_IF)

def read_config():
    print("* Reading configuration file")
    with open('config.json') as fp:
        data = ujson.load(fp)
    return data 

def connect():
    wlan.active(True)
    wlan.config(dhcp_hostname=CONFIG["wifi"]["hostname"])
    if not wlan.isconnected():
        wlan.connect(CONFIG["wifi"]["ssid"], CONFIG["wifi"]["password"])
        while not wlan.isconnected():
            pass

def init():
    global CONFIG 
    CONFIG = read_config()
    global DEVICE_COLORS
    DEVICE_COLORS = {
        'RED': 'a495bb10c5b14b44b5121370f02d74de',
        'GREEN': 'a495bb20c5b14b44b5121370f02d74de',
        'BLACK': 'a495bb30c5b14b44b5121370f02d74de',
        'PURPLE': 'a495bb40c5b14b44b5121370f02d74de',
        'ORANGE': 'a495bb50c5b14b44b5121370f02d74de',
        'BLUE': 'a495bb60c5b14b44b5121370f02d74de',
        'YELLOW': 'a495bb70c5b14b44b5121370f02d74de',
        'PINK': 'a495bb80c5b14b44b5121370f02d74de'
    }

init()
connect()
(_IP, _NETMASK, _GATEWAY, _DNS) = wlan.ifconfig()
gc.collect()