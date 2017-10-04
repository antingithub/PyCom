import machine
from network import WLAN
wlan = WLAN() # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=('192.168.1.200', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('ZON-43A0', auth=(WLAN.WPA2, '7c2b8a22dd92'), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting

print(wlan.ifconfig())
