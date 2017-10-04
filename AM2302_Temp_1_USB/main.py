# DATA PIN G7 for AM2302
# Push button G10



import pycom
import time
from machine import enable_irq, disable_irq,  Pin




# preapre led on P9 = G16
led = Pin('P9', mode=Pin.OUT)
# led callable
led.value(0)
print(led.value())
led.value(1)
print(led.value())

# push button
button = Pin('P10', mode=Pin.IN)
print('PUSH BUTTON STATE = ', button.value())



_LIMIT = const(8)
_BUFFERSIZE = const(1000)

def getval(pin) :
    ms = [1] * _BUFFERSIZE
    mslen = len(ms)
    pin(0)
    time.sleep_us(20000)  # 20ms
    pin(1)
    irqf = disable_irq()  # Disable interrupt requests
    for _ in range(mslen):
        ms[_] = pin()      ## sample input and store value
    enable_irq(irqf)
    #print(ms)
    return ms

def decode(inp):
    res= [0]*5
    bits=[]
    ix = 0
    try:
        if inp[0] == 1 :
            ix = inp.index(0, ix) ## skip to first 0
        ix = inp.index(1,ix) ## skip first 0's to next 1
        ix = inp.index(0,ix) ## skip first 1's to next 0
        while len(bits) < len(res)*8 : ##need 5 * 8 bits :
            ix = inp.index(1,ix) ## index of next 1
            ie = inp.index(0,ix) ## nr of 1's = ie-ix
            bits.append(ie-ix)
            ix = ie
    except Exception as err:
        print (err, ix, len(bits))
        return([0xff,0xff,0xff,0xff])

    for i in range(len(res)):
        for v in bits[i*8:(i+1)*8]:   #process next 8 bit
            res[i] = res[i]<<1  ##shift byte one place to left
            if v > _LIMIT:
                res[i] = res[i]+1  ##and add 1 if lsb is 1

    if (res[0]+res[1]+res[2]+res[3])&0xff != res[4] :   ##parity error!
        print("Checksum Error")
        res= [0xff,0xff,0xff,0xff]

    return(res[0:4])

def DHT11(pin):
    res = decode(getval(pin))

    #  changed by me first the hum then the temp
    hum = 10 * res[0] + res[1]
    temp = 10 * res[2] + res[3]
    return temp, hum

def DHT22(pin) :
    res = decode(getval(pin))
    hum = res[0]*256+res[1]
    temp = res[2]*256 + res[3]
    if (temp > 0x7fff):
        temp = 0x8000 - temp
    return temp, hum

def run():
    # G7 is output also
    # input or output pin in open-drain mode.
    dht_pin=Pin('G7', mode=Pin.OPEN_DRAIN)
    dht_pin(1)

    temp, hum = DHT11(dht_pin)

    temp_str = '{}.{}'.format(temp//10,temp%10)
    hum_str = '{}.{}'.format(hum//10,hum%10)

    # Print or upload it
    print('temp (C) = ', temp_str,'\t', 'RH (%) = ', hum_str)



while True:
    butt = button.value()
    print('PUSH BUTTON STATE = ', butt)
    time.sleep(3)
    run()
