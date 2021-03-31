#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import base64
from scanner._utils import force_unicode

class Track:
    def __init__(self, mfile, path, rootpath):
        idartist = ''
        skip = False
        try:
            self.artist = str(mfile.tags.getall("TPE1")[0])
        except KeyError:
            self.artist = None
        except IndexError:
            self.artist = None
        self.albumartist = None
        try:
            self.albumartist = str(mfile.tags.getall("TPE2")[0])
        except KeyError:
            self.albumartist = None
        except IndexError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        try:
            self.album = str(mfile.tags.getall("TALB")[0])
        except KeyError:
            self.album = None
        except IndexError:
            self.album = None
        self.year = None
        try:
            self.year = int(str(mfile.tags.getall("TDRC")[0]))
        except KeyError:
            self.year = 0
        except IndexError:
            self.year = 0

        # create a def that checks on some chars from an enum; input is the propertie of the file, the output the value
        # do that for all types like number, year and discnumber
        try:
            self.number = int(str(mfile.tags.getall("TRCK")[0]))
        except ValueError:
            try:
                end = str(mfile.tags.getall("TRCK")[0]).index("/")
                self.number = int(str(mfile.tags.getall("TRCK")[0])[0:end])
            except ValueError:
                try:
                    end = str(mfile.tags.getall("TRCK")[0]).index("\\")
                    self.number = int(str(mfile.tags.getall("TRCK")[0])[0:end])
                except ValueError:
                    self.number = None
        except KeyError:
            self.number = None
        except IndexError:
            self.number = None
        try:
            self.title = str(mfile.tags.getall("TIT2")[0])
        except KeyError:
            self.title = None
            skip = True
        except IndexError:
            self.title = None
            skip = True

        self.duration = mfile.info.length * 1000
        #self.path = path.replace("\\", "\\\\")
        self.path = path
        self.path = self.path[len(rootpath):]
        
        self.trackgain = None
        try:
            self.trackgain = self.dbToNum(str(mfile.tags.getall("TXXX:replaygain_track_gain")[0]))
        except KeyError:
            self.trackgain = None
        except IndexError:
            self.trackgain = None
        except ValueError:
            self.trackgain = mfile.info.track_gain

        self.albumgain = None
        try:
            self.albumgain = self.dbToNum(str(mfile.tags.getall("TXXX:replaygain_album_gain")[0]))
        except KeyError:
            self.albumgain = None
        except IndexError:
            self.albumgain = None
        except ValueError:
            self.albumgain = mfile.info.album_gain
        self.disc = None
        try:
            self.disc = int(str(mfile.tags.getall("TPOS")[0]))
        except ValueError:
            try:
                end = str(mfile.tags.getall("TPOS")[0]).index("/")
                self.disc = int(str(mfile.tags.getall("TPOS")[0])[0:end])
            except ValueError:
                try:
                    end = str(mfile.tags.getall("TPOS")[0]).index("\\")
                    self.disc = int(str(mfile.tags.getall("TPOS")[0])[0:end])
                except ValueError:
                    self.disc = None
        except KeyError:
            self.disc = None
        except IndexError:
            self.disc = None
        if skip is not True and idartist and self.album and self.title and (
                self.number is not None):
            self.id = base64.b64encode(bytes(idartist + self.album + str(self.number) + self.title  + '_mp3', 'utf-8')).decode()
        else:
            if skip is not True and idartist and self.album and self.title:
                self.id = base64.b64encode(bytes(idartist + self.album + self.title  + '_mp3', 'utf-8')).decode()
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp3'

    def time(self):
        return self.duration

    def dbToNum(self, string):
        return float(string[: -3])