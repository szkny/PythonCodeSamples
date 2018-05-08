#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image
from optparse import OptionParser

parser = OptionParser()
(Options, Argv) = parser.parse_args()
Argc = len(Argv)

if Argc == 0:
    print(" Usage: tesseract [IMAGE]")
    quit()

# url = "/Users/suzukisohei/Desktop/2048.png"
img = Image.open(Argv[0])
number = pytesseract.image_to_string(img)
print(number)
