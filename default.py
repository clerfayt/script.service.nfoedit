#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import xbmc
import os.path
import xml.dom
import xml.dom.minidom

from resources.lib.helpers import *

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo("name")

dlg = xbmcgui.Dialog()


def createNfoFile(nfoFile, mediaType):
    """ Create a new empty nfo file for the given mediaType """
    nfoContents = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    nfoContents = nfoContents + ("<%s>\n<%s>" % (mediaType,mediaType))
    return writeXmlFile(nfoFile, nfoContents)


def editNfoFile(nfoFile):
    """ Edit the nfo file given by its path """
    #TODO implement loop and accept cancel to quit loop
    cancelled = False
    while not cancelled:
        cancelled = True
        # parse nfo file (get elements with values)
        dom_ = xml.dom.minidom.parse(nfoFile)
        doc = dom_.documentElement
        elements = []
        if doc.nodeType == xml.dom.Node.ELEMENT_NODE:
            mediaType = doc.tagName
            for node in doc.childNodes:
                if node.nodeType == xml.dom.Node.ELEMENT_NODE:
                    if node.firstChild and node.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
                        elements.append((node.tagName, node.firstChild.data))

        if len(elements) > 0:
            elemStrings = []
            for (n,v) in elements: elemStrings.append(n + ": " + v)
            #TODO "Add new element"
            # ask: element to edit
            elem2edit = dlg.select(addonname, elemStrings)
            if elem2edit or elem2edit == 0:
                oldValue = elements[elem2edit][1]
                # ask: new value
                newValue = dlg.input(addonname + (" <%s>" % elements[elem2edit][0]), oldValue, xbmcgui.INPUT_ALPHANUM)
                # change value
                for tag in dom_.getElementsByTagName(elements[elem2edit][0]):
                    if tag.nodeType == xml.dom.Node.ELEMENT_NODE:
                        if tag.firstChild and \
                           tag.firstChild.nodeType == xml.dom.Node.TEXT_NODE and \
                           tag.firstChild.data == oldValue:
                            tag.firstChild.data = newValue
                            break
                else:
                    myNotifyError(transl(30010))
                # overwrite nfo file
                #TODO ask save yes/no
                writeXmlFile(nfoFile, dom_.toxml())
            else:
                myNotify("Done.")
                cancelled = True
        else:
            # TODO "Add element"
            myNotify("No elements found. Done")
            cancelled = True


def writeXmlFile(filepath, xmlContents):
    """Write the given (xml) content to the file given by its path."""
    try:
        f = open(filepath, "w+")
        try:
            f.write(xmlContents)
        except:
            return False
        finally:
            f.close()
    except (IOError, OSError) as e:
        return False
    return True


mode = dlg.select(addonname, [transl(30001), transl(30002)])

if mode == 0:
    """ Edit """
    nfoFile = dlg.browseSingle(1, addonname, "files", ".nfo", False, False)
    if nfoFile:
        editNfoFile(nfoFile)

elif mode == 1:
    """ Create """
    mediaType = dlg.select(addonname, [transl(30003), transl(30004)])
    if mediaType or mediaType == 0:
        mediaType = ["movie", "tvshow", "episodedetails", "artist", "album", "musicvideo"][int(mediaType)]
        # browse for nfo file
        videoFile = dlg.browseSingle(1, addonname, "files", "", False, False)
        if videoFile:
            nfoFile = os.path.splitext(videoFile)[0] + ".nfo"
            if os.path.exists(nfoFile):
                myNotifyWarning(transl(30009))
                editNfoFile(nfoFile)
            elif createNfoFile(nfoFile, mediaType):
                editNfoFile(nfoFile)
