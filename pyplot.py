#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
# from scipy.interpolate import spline
from mymodules.rectselect import RectSelect
from mymodules.keyevent import KeyEvent
import matplotlib as mpl
import matplotlib.pyplot as plt
from optparse import OptionParser
import os
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

parser = OptionParser()
parser.add_option("-t", "--title", dest="title",
                  type="string", default="pyplot",
                  help="window title.")
parser.add_option("-n", "--nload", dest="nload",
                  type="int", default=1,
                  help="load same file NLOAD times.")
parser.add_option("-m", "--marker", dest="marker",
                  type="string", default=None,
                  help="[ '+' | ',' | '.' | '1' | '2' | '3' | '4' ]")
parser.add_option("-l", "--line", dest="line",
                  type="string", default=None,
                  help="[ '-' | '--' | '-.' | ':' | 'steps' | 'steps-mid']")
parser.add_option("-e", "--error", dest="error",
                  action="store_true", default=False,
                  help="draw error bar using next column.")
parser.add_option("-u", "--using", dest="column", type="int",
                  action='append', default=[],
                  help="use column line for FILE")
parser.add_option("-c", "--color", dest="color",
                  type="string", default=None,
                  help="line(marker) color")
parser.add_option("-s", "--save", dest="save",
                  type="string", default=None,
                  help="save as image")
parser.add_option("-w", "--width", dest="width",
                  type="float", default=0.8,
                  help="set line width")
parser.add_option("-L", "--legend",
                  action="store_true", default=False,
                  help="legend flag")
parser.add_option("--xlabel", dest="xlabel",
                  type="string", default="",
                  help="x-axis name.")
parser.add_option("--ylabel", dest="ylabel",
                  type="string", default="",
                  help="y-axis name.")
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
parser.add_option("--xlog",
                  action="store_true", default=False,
                  help="log scale xaxis")
parser.add_option("--ylog",
                  action="store_true", default=False,
                  help="log scale yaxis")
(Options, Argv) = parser.parse_args()
Argc = len(Argv)


def main(FileNum, FileName):
    if (FileNum == 0):
        print(" Usage: pyplot [FILENAME]")
        quit()
    CheckData(FileName)
    figure = CanvasSet()
    LoadData(FileNum, FileName)
    ShowGraph(FileNum, figure)


def CheckData(FileName):
    ncolumn = 0
    try:
        for line in open(FileName[0], "r"):
            if line == "\n":
                continue
            if line[0] == "/" and line[1] == "/":
                continue
            if line[0] == "#":
                continue
            ncolumn = len(line.split())
            if ncolumn != 0:
                break
    except OSError:
        print(" error: file not found.  —— %s" % FileName[0])
        quit()
    except ():
        print(" error: something wrong.")
        quit()

    if ncolumn == 1:
        print("ploting by 'pyhist' because this is one-dimensional data.")
        maped_list = map(str, FileName)
        file_name = ' '.join(maped_list)
        os.system("pyhist %s" % file_name)
        quit()


def CanvasSet():
    fig = plt.figure(figsize=(7, 5))
    fig.canvas.set_window_title(Options.title)
    fig.patch.set_facecolor("white")
    fig.patch.set_alpha(1)
    sub = fig.add_subplot(111)
    sub.patch.set_facecolor("white")
    sub.patch.set_alpha(1)
    sub.set_axisbelow(True)

    flag = False
    for k, v in os.environ.items():
        if k == 'MPLBACKEND':
            flag = True
    if bool(flag) is False:
        fig.canvas.manager.window.attributes('-topmost', 1)
    return fig


def LoadData(FileNum, FileName):
    # cmap = plt.get_cmap("Set1")
    column = Options.column
    AddFileNum = 0
    if Options.nload > 1:
        for i in range(1, Options.nload):
            FileName.insert(1, FileName[0])
            AddFileNum += 1
    counter = 0
    LenOptionColumn = len(Options.column)
    for i in range(0, FileNum+AddFileNum):
        root, ext = os.path.splitext(FileName[i])

        DotFlag = LineStyle(i, counter)
        # colormap = cmap(float(counter)/(FileNum*2))
        color = MakeColor(counter)
        if i >= AddFileNum:
            counter += 1

        if len(column) <= i+1:
            if LenOptionColumn == 1:
                column.append(Options.column[0])
            else:
                column.append(1)

        if ext == ".txt":
            LoadTxt(FileName[i], column[i], color, DotFlag)
        else:
            print(" error: invalid extension.  —— %s" % FileName[i])
            quit()


def LoadTxt(FileName, column, linecolor, DotFlag):
    try:
        data = np.loadtxt(FileName, comments="//", usecols=(0, column))
    except ValueError:
        data = np.loadtxt(FileName, comments="#", usecols=(0, column))
    # except ValueError:
    #     data = np.loadtxt(FileName, comments="*", usecols=(0, column))
    except (ValueError, IndexError) as e:
        print(" error: invalid file format. —— %s   " % FileName, e)
        print("        if you want to comment out, ",
              "you can use '//', '#' or '*' in the text file.")
        quit()
    # x_smooth = np.linspace(min(data[:, 0]), max(data[:, 0]), 100)
    # y_smooth = spline(data[:, 0], data[:, 1], x_smooth)
    # print(y_smooth)
    if DotFlag:
        line = "--"
    else:
        line = Options.line
    # plt.plot(x_smooth, y_smooth,
    plt.plot(data[:, 0], data[:, 1],
             marker=Options.marker,
             linestyle=line,
             color=linecolor,
             markersize=5.0,
             linewidth=Options.width,
             label=FileName)
    if Options.error:
        try:
            err = np.loadtxt(FileName, comments="//", usecols=column+1)
        except ValueError:
            err = np.loadtxt(FileName, comments="#", usecols=column+1)
        # except ValueError:
        #     err = np.loadtxt(FileName, comments="*", usecols=column+1)
        except (ValueError, IndexError) as e:
            print(" error: invalid file format. —— %s   " % FileName, e)
            print("        if you want to comment out,\
                  you can use '//', '#' or '*' in the text file.")
            quit()
        plt.errorbar(data[:, 0], data[:, 1], yerr=err,
                     fmt='.',
                     color='blue',
                     linewidth=0.5)


def ShowGraph(FileNum, fig):
    if Options.legend and FileNum <= 10:
        plt.legend()
    plt.xlabel(Options.xlabel)
    plt.ylabel(Options.ylabel)
    plt.grid(True)
    # plt.grid(which='both')
    if Options.xlog:
        plt.xscale('log')
    if Options.ylog:
        plt.yscale('log')
    plt.xlim([Options.xmin, Options.xmax])
    plt.ylim([Options.ymin, Options.ymax])
    RectSelect()
    KeyEvent()
    if Options.save is None:
        plt.show()
    else:
        plt.savefig(Options.save)


def MakeColor(counter):
    mpl.style.use('default')
    color = 'C%d' % counter
    if Options.color is not None:
        color = Options.color
    return color


def LineStyle(i, counter):
    if i != 0 and counter == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    main(Argc, Argv)
