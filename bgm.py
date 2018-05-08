#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from optparse import OptionParser
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

parser = OptionParser()
parser.add_option("-l", "--loop", dest="loop",
                  type="int", default=1,
                  help="repeat play list [LOOP]-times.")
parser.add_option("-r", "--rock", dest="rock",
                  action="store_true", default=False,
                  help="play rock.")
parser.add_option("-j", "--jazz", dest="jazz",
                  action="store_true", default=False,
                  help="play jazz.")
parser.add_option("-c", "--chill", dest="chill",
                  action="store_true", default=False,
                  help="play chill-hop.")
(Options, Argv) = parser.parse_args()
Argc = len(Argv)


path = "/Users/suzukisohei/Downloads/mps/"
rock = "/Users/suzukisohei/Music/downloads/rock"
jazz = "/Users/suzukisohei/Music/downloads/jazz"


def main(Argc,Argv):
    play = path
    if Options.rock:
        play = rock
    elif Options.jazz:
        play = jazz
    elif Options.chill:
        os.system("mpsyt playurl AQBh9soLSkI")
        quit()
    command = "mpv --shuffle --no-video"
    for i in range(Options.loop):
        command = command + " %s" % play
    os.system(command)

if __name__ == "__main__":
    main(Argc, Argv)
