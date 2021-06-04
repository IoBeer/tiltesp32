import ujson
import network
import gc

wlan = network.WLAN(network.STA_IF)

def read_config():
    print("* Reading configuration file")
    with open('config.json') as fp:
        data = ujson.load(fp)
    return data 

def connect():
    wlan.active(True)
    wlan.config(dhcp_hostname=config["wifi"]["hostname"])
    if not wlan.isconnected():
        wlan.connect(config["wifi"]["ssid"], config["wifi"]["password"])
        while not wlan.isconnected():
            pass

config = read_config()
connect()
(ip, netmask, gateway, dns) = wlan.ifconfig()
gc.collect()