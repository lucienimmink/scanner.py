#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import base64
import _utils as utils


class Track:
    def __init__(self, mfile, path, rootpath):
        idartist = ''
        self.artist = mfile['\xa9ART'][0]
        self.albumartist = None
        try:
            self.albumartist = mfile['aART'][0]
        except KeyError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        self.album = mfile['\xa9alb'][0]
        self.year = None
        try:
            self.year = mfile['\xa9day'][0]
        except KeyError:
            self.year = 0
        self.number = mfile['trkn'][0][0]
        self.title = mfile['\xa9nam'][0]

        self.duration = mfile.info.length * 1000
        self.path = utils.force_unicode(path, "utf-8").replace("\\", "\\\\")
        self.path = self.path[len(rootpath):]
        self.disc = None
        try:
            self.disc = mfile['disk'][0][0]
        except KeyError:
            self.disc = 1
        if idartist and self.album and self.title and (self.number is
                                                       not None):
            self.id = base64.b64encode(
                (utils.force_unicode(idartist, 'utf-8') + utils.force_unicode(
                    self.album, 'utf-8') + str(self.number) + utils.
                 force_unicode(self.title, 'utf-8')).encode('utf-8') + '_flac')
        else:
            if idartist and self.album and self.title:
                self.id = base64.b64encode(
                    (utils.force_unicode(idartist, 'utf-8') + utils.
                     force_unicode(self.album, 'utf-8') + utils.force_unicode(
                         self.title, 'utf-8')).encode('utf-8') + '_flac')
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp4'

    def time(self):
        return self.duration