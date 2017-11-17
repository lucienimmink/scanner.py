#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import base64
import _utils as utils


class Track:
    def __init__(self, mfile, path, rootpath):
        idartist = ''
        skip = False
        try:
            self.artist = mfile['artist'][0]
        except KeyError:
            self.artist = None
        self.albumartist = None
        try:
            self.albumartist = mfile['albumartist'][0]
        except KeyError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        try:
            self.album = mfile['album'][0]
        except KeyError:
            self.album = None
        self.year = None
        try:
            self.year = mfile['date'][0]
        except KeyError:
            self.year = 0

        # create a def that checks on some chars from an enum; input is the propertie of the file, the output the value
        # do that for all types like number, year and discnumber
        try:
            self.number = int(mfile['tracknumber'][0])
        except ValueError:
            try:
                end = mfile['tracknumber'][0].index("/")
                self.number = int(mfile['tracknumber'][0][0:end])
            except ValueError:
                try:
                    end = mfile['tracknumber'][0].index("\\")
                    self.number = int(mfile['tracknumber'][0][0:end])
                except ValueError:
                    self.number = None
        except KeyError:
            self.number = None
        try:
            self.title = mfile['title'][0]
        except KeyError:
            self.title = None
            skip = True

        self.duration = mfile.info.length * 1000
        self.path = utils.force_unicode(path, "utf-8").replace("\\", "\\\\")
        self.path = self.path[len(rootpath):]
        self.disc = None
        try:
            self.disc = int(mfile['discnumber'][0])
        except ValueError:
            try:
                end = mfile['discnumber'][0].index("/")
                self.disc = int(mfile['discnumber'][0][0:end])
            except ValueError:
                try:
                    end = mfile['discnumber'][0].index("\\")
                    self.disc = int(mfile['discnumber'][0][0:end])
                except ValueError:
                    self.disc = None
        except KeyError:
            self.disc = None
        if skip is not True and idartist and self.album and self.title and (
                self.number is not None):
            self.id = base64.b64encode(
                (utils.force_unicode(idartist, 'utf-8') +
                 utils.force_unicode(self.album, 'utf-8') + str(self.number) +
                 utils.force_unicode(self.title, 'utf-8')).encode('utf-8') + '_mp3')
        else:
            if skip is not True and idartist and self.album and self.title:
                self.id = base64.b64encode(
                    (utils.force_unicode(idartist, 'utf-8') +
                     utils.force_unicode(self.album, 'utf-8') + utils.force_unicode(
                         self.title, 'utf-8')).encode('utf-8') + '_mp3')
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp3'

    def time(self):
        return self.duration
