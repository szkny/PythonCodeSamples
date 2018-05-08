#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import requests
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--screenshot",
                  action="store_true", default=False,
                  help="Capture and Send Screen Shot.")
parser.add_option("-i", "--image", dest="image",
                  type="string", default=None,
                  help="Send image file.")
parser.add_option("-f", "--file", dest="file",
                  type="string", default=None,
                  help="Send Text file.")
(Options, Argv) = parser.parse_args()
Argc = len(Argv)

def main(Argc, Argv):
    line_notify_token = '3FtQaM2Sqwig2NZycSwD4Cg52lLOYXjyC3SCac1Nwza'
    line_notify_api   = 'https://notify-api.line.me/api/notify'
    payload = {'message': Message()}
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    if Options.screenshot:
        screenshot = "/Users/suzukisohei/ScreenShot/hogehogewhale.png"
        capture = "screencapture %s" % screenshot
        remove = "rm %s" % screenshot
        os.system(capture)
        sendfile = {"imageFile": open(screenshot, "rb")}
        requests.post(line_notify_api, data=payload,
                      headers=headers, files=sendfile)
        os.system(remove)

    elif Options.image is not None:
        if os.path.exists(Options.image):
            sendfile = {"imageFile": open(Options.image, "rb")}
            requests.post(line_notify_api, data=payload,
                          headers=headers, files=sendfile)
        else:
            print(" image file not found : '%s' " % Options.image)

    else:
        requests.post(line_notify_api, data=payload, headers=headers)


def Message():
    if Options.file is not None:
        if Argc == 0:
            message = Options.file + "\n"
        else:
            message = Argv[0] + "\n"
        fp = open(Options.file, "r")
        for row in fp:
            message += row
        fp.close()
    elif Argc == 0:
        message = Options.image
    else:
        message = Argv[0]

    if message is None:
        message = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    return message


if __name__ == "__main__":
    main(Argc, Argv)
