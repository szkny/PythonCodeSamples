import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector

class RectSelect(object):
    def __init__(self, ax=None):
        self.ax = ax or plt.gca()
        self.rect = Rectangle((0,0), 0, 0, color='orange', alpha=0.5)
        self.ax.add_patch(self.rect)
        self.blc = np.zeros(2)
        self.trc = np.zeros(2)

        def selector(event):
            if event.key in ['R', 'r']:
                if selector.RS.active:
                    print ('RectSelect deactivated.')
                    selector.RS.set_active(False)
                else:
                    print ('RectSelect activated.')
                    selector.RS.set_active(True)

        selector.RS = RectangleSelector(self.ax, self.callback)
        self.ax.figure.canvas.mpl_connect('key_press_event', selector)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.release)
        selector.RS.set_active(False)

    def callback(self, eclick, erelease):
        x0, x1 = eclick.xdata, erelease.xdata
        y0, y1 = eclick.ydata, erelease.ydata
        self.blc = min(x0, x1), min(y0, y1)
        self.trc = max(x0, x1), max(y0, y1)
        blc_print = '({:0.4},{:0.4})'.format(*self.blc)
        trc_print = '({:0.4},{:0.4})'.format(*self.trc)
        print('blc={}, trc={}'.format(blc_print, trc_print))

    def release(self, event):
        self.rect.set_width(self.trc[0] - self.blc[0])
        self.rect.set_height(self.trc[1] - self.blc[1])
        self.rect.set_xy(self.blc)
        self.ax.figure.canvas.draw()
