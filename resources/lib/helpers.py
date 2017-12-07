#!/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

def transl(translationId):
    """Returns the translated string with the given id."""
    return xbmcaddon.Addon().getLocalizedString(translationId).encode("utf-8")

def myNotify(message, header=None, time_=3000, icon=None):
    """Send notification. If header==None the addon-name is used.
       If icon==None the addon-icon is used.
    """
    _addon = xbmcaddon.Addon()
    header = _addon.getAddonInfo('name') if not header else header
    icon   = _addon.getAddonInfo('icon') if not icon else icon
    xbmcgui.Dialog().notification(header, message, icon, time_)

def myNotifyError(message, header=None, time_=3000):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_ERROR)

def myNotifyWarning(message, header=None, time_=3000):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_WARNING)

def myNotifyInfo(message, header=None, time_=3000):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_INFO)

def myLog(message, level=xbmc.LOGNOTICE):
    """Log a message."""
    output = "[nfoEDIT]: " + message
    xbmc.log(msg=output, level=level)
