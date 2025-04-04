#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import base64
from scanner._utils import force_unicode


class Track:
    def __init__(self, mfile, path, rootpath):
        idartist = ''
        self.artist = None
        try:
            self.artist = mfile['\xa9ART'][0]
        except KeyError:
            try:
                self.artist = mfile['aART'][0]
            except KeyError:
                self.artist = None
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
        #self.path = path.replace("\\", "\\\\")
        self.path = path
        self.path = self.path[len(rootpath):]
        self.trackgain = None
        try:
            self.trackgain = self.dbToNum(mfile['----:com.apple.iTunes:replaygain_track_gain'][0].decode('utf-8'))
        except KeyError:
            self.trackgain = None
        self.albumgain = None
        try:
            self.albumgain = self.dbToNum(mfile['----:com.apple.iTunes:replaygain_album_gain'][0].decode('utf-8'))
        except KeyError:
            self.albumgain = None
        self.disc = None
        try:
            self.disc = mfile['disk'][0][0]
        except KeyError:
            self.disc = 1
        self.samplerate = None
        try:
            self.samplerate = mfile.info.sample_rate
        except AttributeError:
            self.samplerate = None
        self.bitrate = None
        try:
            self.bitrate = mfile.info.bitrate
        except AttributeError:
            self.bitrate = None
        self.bits_per_sample = None
        try:
            self.bits_per_sample = mfile.info.bits_per_sample
        except AttributeError:
            self.bits_per_sample = None
        self.channels = None
        try:
            self.channels = mfile.info.channels
        except AttributeError:
            self.channels = None
        
        if idartist and self.album and self.title and (self.number is
                                                       not None):
            self.id = base64.b64encode(bytes(idartist + self.album + str(self.disc) + str(self.number) + self.title  + '_mp4', 'utf-8')).decode()
        else:
            if idartist and self.album and self.title:
                self.id = base64.b64encode(bytes(idartist + self.album + self.title  + '_mp4', 'utf-8')).decode()
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp4'

    def time(self):
        return self.duration

    def dbToNum(self, string):
        return float(string[: -3])