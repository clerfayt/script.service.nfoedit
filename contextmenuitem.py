#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcgui

from resources.lib.utils import *
from resources.lib.nfoedit import *


if MySettings.contextMenuItemHidden():
    xbmcgui.Window(10000).setProperty("NFOEDIT_HIDEMENUITEM", "True")
else:
    xbmcgui.Window(10000).setProperty("NFOEDIT_HIDEMENUITEM", "")
    xbmcgui.Window(10000).clearProperty("NFOEDIT_HIDEMENUITEM")


def main():
    filepath = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    if not filepath:
        myNotifyError(transl(30024))
    else:
        nfoFile = os.path.splitext(filepath)[0] + ".nfo"
        nfoedit = NfoEdit()
        if os.path.exists(nfoFile):
            nfoedit.runModeEdit(nfoFile)
        else:
            info = sys.listitem.getVideoInfoTag()
            mediaType = info.getMediaType();
            if mediaType == "episode":
                mediaType = "episodedetails"
            else:
                mediaType = "movie"
            nfoedit.runModeCreate(nfoFile, mediaType)

if __name__ == '__main__':
    main()
