#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import xbmc
import os.path
import xml.dom
import xml.dom.minidom

from .helpers import *


class NfoEdit():
    """Class handling the process of editing an NFO file."""
    def __init__(self):
        self.dlg = xbmcgui.Dialog()

    def createNfoFile(self, nfoFile, mediaType):
        """ Create a new empty nfo file for the given mediaType """
        nfoContents = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        nfoContents = nfoContents + ("<%s>\n</%s>" % (mediaType,mediaType))
        return self.writeXmlFile(nfoFile, nfoContents)

    def editNfoFile(self, nfoFile):
        """ Edit the nfo file given by its path """
        #endless loop until cancelled by user input
        cancelled = False
        while not cancelled:
            # parse nfo file (get elements with values)
            dom_ = xml.dom.minidom.parse(nfoFile)
            doc = dom_.documentElement
            elements = [("::", " " + transl(30011) + "  :::")]  # "D O N E  /  E N D"

            if doc.nodeType == xml.dom.Node.ELEMENT_NODE:
                mediaType = doc.tagName
                for node in doc.childNodes:
                    if node.nodeType == xml.dom.Node.ELEMENT_NODE:
                        if node.firstChild and node.firstChild.nodeType == xml.dom.Node.TEXT_NODE:
                            elements.append((node.tagName, node.firstChild.data))

            elements.append(("::", " " + transl(30012) + "  :::"))  # "New Element"
            elements.append(("::", " " + transl(30025) + "  :::"))  # "Show Help"
            elemStrings = []
            for (n,v) in elements: elemStrings.append(n + ": " + v)

            # ask: element to edit (or cancel or newElement)
            elem2edit = self.dlg.select(ADDONNAME, elemStrings)
            if elem2edit > 0 and elem2edit < len(elements)-2:
                oldValue = elements[elem2edit][1]
                # ask: new value
                newValue = self.dlg.input(ADDONNAME + (" <%s>" % elements[elem2edit][0]),
                                          oldValue, xbmcgui.INPUT_ALPHANUM)
                if newValue != "" or self.dlg.yesno(ADDONNAME + (" <%s>" % elements[elem2edit][0]),
                                                    transl(30013)):
                    # if supplied new value or ClearValue?==yes : change value
                    for tag in dom_.getElementsByTagName(elements[elem2edit][0]):
                        if tag.nodeType == xml.dom.Node.ELEMENT_NODE:
                            if tag.firstChild and \
                               tag.firstChild.nodeType == xml.dom.Node.TEXT_NODE and \
                               tag.firstChild.data == oldValue:
                                tag.firstChild.data = newValue
                                break
                    else:
                        myNotifyError(transl(30010))  #"Could not change value."
                    self.saveChanges(nfoFile, dom_)
                else:
                    myNotify(transl(30016))  #"Did not change value."
            elif elem2edit == len(elements)-2:  #before last => new element
                newElemName = self.dlg.input(transl(30014))  #"New tag name?"
                if newElemName:
                    newValue = self.dlg.input(transl(30015))  #"New value?"
                    if newValue:
                        newElem_dom = dom_.createElement(newElemName)
                        newElem_dom.appendChild(dom_.createTextNode(newValue))
                        doc.appendChild(newElem_dom)
                        self.saveChanges(nfoFile, dom_)
                    else:
                        myNotify(transl(30017))  #"Did not add new element."
                else:
                    myNotify(transl(30017))  #"Did not add new element."
            elif elem2edit == len(elements)-1:  #last => show help
                self.dlg.textviewer(transl(30026), transl(30027))
            else:
                myNotify(transl(30018), sound=False)  #"Finished"
                cancelled = True


    def saveChanges(self, filepath, dom_):
        """Save the given dom to file. Maybe ask before saving."""
        if not MySettings.askBeforeSave() or self.dlg.yesno(ADDONNAME, transl(30021)):
            # overwrite nfo file
                self.writeXmlFile(filepath, dom_.toprettyxml(encoding="UTF-8"))


    def writeXmlFile(self, filepath, xmlContents):
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


    def runModeEdit(self, nfoFile):
        """Mode: edit."""
        if nfoFile:
            self.editNfoFile(nfoFile)        


    def runModeCreate(self, nfoFile, mediaType):
        """Mode: create."""
        if nfoFile and os.path.exists(nfoFile):
            myNotifyWarning(transl(30009))
            self.editNfoFile(nfoFile)
        elif nfoFile and self.createNfoFile(nfoFile, mediaType):
            self.editNfoFile(nfoFile)


    def runModeShow(self, nfoFile):
        """Mode: show."""
        if nfoFile and os.path.exists(nfoFile):
            with file(nfoFile) as f: contents = f.read()
            self.dlg.textviewer(os.path.split(nfoFile)[1], contents)

    
    def runCompletely(self):
        mode = self.dlg.select(ADDONNAME, [transl(30001), transl(30002), transl(30019)])

        if mode == 0:
            """ Edit """
            nfoFile = self.dlg.browseSingle(1, ADDONNAME, "files", ".nfo", False, False)
            self.runModeEdit(nfoFile)

        elif mode == 1:
            """ Create """
            mediaType = self.dlg.select(ADDONNAME, [transl(30003), transl(30004)])
            if mediaType or mediaType == 0:
                mediaType = ["movie", "tvshow", "episodedetails", "artist", "album", "musicvideo"][int(mediaType)]
                # browse for nfo file
                videoFile = self.dlg.browseSingle(1, ADDONNAME, "files", "", False, False)
                if videoFile:
                    nfoFile = os.path.splitext(videoFile)[0] + ".nfo"
                    self.runModeCreate(nfoFile, mediaType)

        elif mode == 2:
            """ Show existing file's contents """
            nfoFile = self.dlg.browseSingle(1, ADDONNAME, "files", ".nfo", False, False)
            self.runModeShow(nfoFile)

        #elif mode == -1: #cancel
