#!/usr/bin/env python3
 
from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.render import canvas
from PIL import ImageDraw, ImageFont
 
import socket
import fcntl
import struct
#from subprocess import Popen,PIPE
import time 

def getIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', ifname[:15].encode('utf-8')) 
    )[20:24])
 
def stats(oled):
    font = ImageFont.load_default()
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 14)
    with canvas(oled) as draw:
        draw.text((2, 5), "IP: " + getIP("wlan0"), font=font2, fill=255)
 
 
def main():
    time.sleep(10);
    serial = i2c(port=1, address=0x3C)
    oled = sh1106(serial)
    stats(oled)
    time.sleep(60*60)
 
if __name__ == "__main__":
    main()
