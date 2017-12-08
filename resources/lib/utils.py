#!/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()
ADDONNAME = ADDON.getAddonInfo('name')

def transl(translationId):
    """Returns the translated string with the given id."""
    return ADDON.getLocalizedString(translationId).encode("utf-8")

def myNotify(message, header=None, time_=3000, icon=None, sound=True):
    """Send notification. If header==None the addon-name is used.
       If icon==None the addon-icon is used.
    """
    header = ADDONNAME if not header else header
    icon   = ADDON.getAddonInfo('icon') if not icon else icon
    xbmcgui.Dialog().notification(header, message, icon, time_, sound)

def myNotifyError(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_ERROR, sound)

def myNotifyWarning(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_WARNING, sound)

def myNotifyInfo(message, header=None, time_=3000, sound=True):
    myNotify(message, header, time_, xbmcgui.NOTIFICATION_INFO, sound)

def myLog(message, level=xbmc.LOGNOTICE):
    """Log a message."""
    output = "[nfoEDIT]: " + message
    xbmc.log(msg=output, level=level)

class MySettings:
    """Helper class with static methods for retrieving settings values."""
    _addon = xbmcaddon.Addon()
    @staticmethod
    def askBeforeSave():
        return MySettings._addon.getSetting("askBeforeSave") == "true"
    @staticmethod
    def contextMenuItemHidden():
        return MySettings._addon.getSetting("contextMenuItemHidden") == "true"
