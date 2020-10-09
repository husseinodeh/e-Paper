#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13
import time
from PIL import Image,ImageDraw,ImageFont
import traceback


epd = epd2in13.EPD()
epd.init(epd.lut_full_update)
#epd.Clear(0xFF)

# Drawing on the image
fonts = os.path.join(picdir, 'Font.ttc')
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)


time_image = Image.new('1', (epd.height, epd.width), 0)
time_draw = ImageDraw.Draw(time_image)
#time_draw.rectangle((0, 0, 249, 121), fill = 0)
import socket
time_draw.text((0, 0), "local IP: "+([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]), font = ImageFont.truetype(fonts,20), fill = 255)

import urllib.request

time_draw.text((0, 0),"public IP: "+urllib.request.urlopen('https://ident.me').read().decode('utf8'), font = font15, fill = 255)

#    time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
epd.display(epd.getbuffer(time_image))
