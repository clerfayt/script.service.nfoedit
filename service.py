#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcgui

from resources.lib.utils import *


class MyMonitor(xbmc.Monitor):
    """ Monitor of settings """
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.updateContextMenuItem()

    def onSettingsChanged(self):
        self.updateContextMenuItem()

    def updateContextMenuItem(self):
        if MySettings.contextMenuItemHidden():
            xbmcgui.Window(10000).setProperty("NFOEDIT_HIDEMENUITEM", "True")
        else:
            xbmcgui.Window(10000).setProperty("NFOEDIT_HIDEMENUITEM", "")
            xbmcgui.Window(10000).clearProperty("NFOEDIT_HIDEMENUITEM")


if __name__ == "__main__":
    monitor = MyMonitor()
    while not monitor.abortRequested():
        #wait 60sec for Kodi to quit
        if monitor.waitForAbort(60):
            break
    del monitor
