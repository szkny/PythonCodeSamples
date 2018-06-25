#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mymodules.keyevent import KeyEvent
from optparse import OptionParser
import os.path
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

parser = OptionParser()
parser.add_option("-a", "--add", dest="add",
                  action="store_true", default=False,
                  help="add FILES to histogram")
parser.add_option("-u", "--using", dest="column",
                  type="int", default=0,
                  help="use column line")
parser.add_option("-t", "--type", dest="type",
                  type="string", default="step",
                  help="[ 'bar' | 'barstacked' | 'step' | 'stepfilled' ]")
parser.add_option("-c", "--color", dest="color",
                  type="string", default=None,
                  help="color")
parser.add_option("-b", "--bins", dest="bins",
                  type="int", default=50,
                  help="number of bins")
parser.add_option("-L", "--legend",
                  action="store_true", default=False,
                  help="legend flag")
parser.add_option("--xmax", dest="xmax",
                  type="float", default=None,
                  help="maximum of x range")
parser.add_option("--xmin", dest="xmin",
                  type="float", default=None,
                  help="minimum of x range")
parser.add_option("--ymax", dest="ymax",
                  type="float", default=None,
                  help="maximum of y range")
parser.add_option("--ymin", dest="ymin",
                  type="float", default=None,
                  help="minimum of y range")
(Options, Argv) = parser.parse_args()
Argc = len(Argv)


def main(FileNum, FileName):
    if (FileNum == 0):
        print(" usage: pyhist FILENAME")
        quit()
    CanvasSet()
    LoadData(FileNum, FileName)
    ShowGraph(FileNum)


def CanvasSet():
    fig = plt.figure(figsize=(7, 5))
    fig.canvas.set_window_title("pyplot")
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(1)
    sub = fig.add_subplot(111)
    sub.patch.set_facecolor("white")
    sub.patch.set_alpha(1)
    sub.set_axisbelow(True)
    # sub.grid(color='gray', linestyle='dashed')
    flag = False
    for k, v in os.environ.items():
        if k == 'MPLBACKEND':
            flag = True
    if bool(flag) is False:
        fig.canvas.manager.window.attributes('-topmost', 1)


data = []


def LoadData(FileNum, FileName):
    Flag = False
    for i in range(0, FileNum):
        if i == FileNum-1:
            Flag = True
        root, ext = os.path.splitext(FileName[i])
        if ext == ".txt":
            LoadTxt(Flag, FileName[i])

        elif ext == ".csv":
            LoadCsv(Flag, FileName[i])

        else:
            print(" error: invalid extension. —— %s" % FileName[i])
            quit()


def LoadTxt(Flag, FileName):
    global data
    try:
        data = np.loadtxt(FileName, comments="//",
                          usecols=(Options.column), ndmin=1)
    # except ValueError:
    #     data = np.loadtxt(FileName, comments="#",
    #                       usecols=(Options.column), ndmin=1)
    except ValueError as e:
        print(" error: invalid file format. —— %s   " % FileName, e)
        quit()

    if Options.xmin is None or Options.xmax is None:
        rangeoption = None
    else:
        rangeoption = (Options.xmin, Options.xmax)

    if Options.add is False:
        plt.hist(data,
                 histtype=Options.type,
                 color=Options.color,
                 range=rangeoption,
                 bins=Options.bins,
                 label=FileName)
        data = []
    elif Flag:
        plt.hist(data,
                 histtype=Options.type,
                 color=Options.color,
                 range=rangeoption,
                 bins=Options.bins,
                 label=FileName)


def LoadCsv(Flag, FileName):
    global data
    try:
        data = np.loadtxt(FileName, comments="//", delimiter=",",
                          usecols=(Options.column), ndmin=1)
    # except ValueError:
    #     data = np.loadtxt(FileName, comments="#", delimiter=",",
    #                       usecols=(Options.column), ndmin=1)
    except ValueError as e:
        print(" error: invalid format. —— %s   " % FileName, e)
        quit()

    if Options.xmin is None or Options.xmax is None:
        rangeoption = None
    else:
        rangeoption = (Options.xmin, Options.xmax)

    if Options.add is False:
        plt.hist(data,
                 histtype=Options.type,
                 color=Options.color,
                 range=rangeoption,
                 bins=Options.bins,
                 label=FileName)
        data = []
    elif Flag:
        plt.hist(data,
                 histtype=Options.type,
                 color=Options.color,
                 range=rangeoption,
                 bins=Options.bins,
                 label=FileName)


def ShowGraph(FileNum):
    if Options.legend and FileNum <= 10:
        plt.legend()
    plt.grid(True)
    plt.xlim([Options.xmin, Options.xmax])
    plt.ylim([Options.ymin, Options.ymax])
    KeyEvent()
    plt.show()


if __name__ == "__main__":
    main(Argc, Argv)
