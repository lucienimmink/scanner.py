#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This program is made possible by the awesome python knowledge of my darling Ivana <3 for ever"""

import os, fnmatch, json, sys, codecs, time, argparse, logging, base64
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp3 import EasyMP3 as MP3

parser = argparse.ArgumentParser(description='Scans a given directory for MP3\'s and places the output file in an optional directory');
parser.add_argument('scanpath', metavar='scanpath', help='directory to scan')
parser.add_argument('--destpath', metavar='destination path', help='directory to place the output json in')
args = parser.parse_args()

rootpath = args.scanpath
destpath = args.destpath or args.scanpath

""" logging """
logging.basicConfig(filename='scanner.log', level=logging.DEBUG)

f = codecs.open(destpath + '/node-music.json', 'w', "utf-8")
p = codecs.open(destpath + '/progress.txt', 'w', "utf-8")

jsonFile = list()
nrScanned = 0
total_files = 0
totalTime = 0
start = time.time()

class MP3Track:
    def __init__ (self, file, path):
        idartist = ''
        skip = False
        try:
            self.artist = file['artist'][0]
        except KeyError:
            self.artist = None
        self.albumartist = None
        try:
            self.albumartist = file['albumartist'][0]
        except KeyError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        self.album = file['album'][0]
        self.year = None
        try:
            self.year = file['date'][0]
        except KeyError:
            self.year = 0
        try:
            self.number = int(file['tracknumber'][0])
        except ValueError:
            end = file['tracknumber'][0].index("/")
            self.number = int(file['tracknumber'][0][0:end])
        except KeyError:
            self.number = None
        try:
            self.title = file['title'][0]
        except KeyError:
            self.title = None
            skip = True

        self.duration = file.info.length * 1000
        self.path = _force_unicode(path, "utf-8").replace("\\", "\\\\")
        self.path = self.path[len(rootpath):]
        self.disc = None
        try:
            self.disc = int(file['discnumber'][0])
        except ValueError:
            end = file['discnumber'][0].index("/")
            self.disc = int(file['discnumber'][0][0:end])
        except KeyError:
            self.disc = None
        if skip is not True and idartist and self.album and self.title and (self.number is not None):
            self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + str(self.number) + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_mp3')
        else:
            if skip is not True and idartist and self.album and self.title:
                self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_mp3')
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp3'
    def time(self):
        return self.duration

class FlacTrack:
    def __init__ (self, file, path):
        idartist = ''
        self.artist = file['artist'][0]
        self.albumartist = None
        try:
            self.albumartist = file['albumartist'][0]
        except KeyError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        self.album = file['album'][0]
        self.year = None
        try:
            self.year = file['date'][0]
        except KeyError:
            self.year = 0
        self.number = int(file['tracknumber'][0])
        self.title = file['title'][0]

        self.duration = file.info.length * 1000
        self.path = _force_unicode(path, "utf-8").replace("\\", "\\\\")
        self.path = self.path[len(rootpath):]
        self.disc = None
        try:
            self.disc = int(file['discnumber'][0])
        except KeyError:
            self.disc = 1
        if idartist and self.album and self.title and (self.number is not None):
            self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + str(self.number) + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_flac')
        else:
            if idartist and self.album and self.title:
                self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_flac')
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'flac'
    def time(self):
        return self.duration

class MP4Track:
    def __init__ (self, file, path):
        idartist = ''
        self.artist = file['\xa9ART'][0]
        self.albumartist = None
        try:
            self.albumartist = file['aART'][0]
        except KeyError:
            self.albumartist = None

        if self.artist is not None:
            idartist = self.artist
        if self.albumartist is not None:
            idartist = self.albumartist
        self.album = file['\xa9alb'][0]
        self.year = None
        try:
            self.year = file['\xa9day'][0]
        except KeyError:
            self.year = 0
        self.number = file['trkn'][0][0]
        self.title = file['\xa9nam'][0]

        self.duration = file.info.length * 1000
        self.path = _force_unicode(path, "utf-8").replace("\\", "\\\\")
        self.path = self.path[len(rootpath):]
        self.disc = None
        try:
            self.disc = file['disk'][0][0]
        except KeyError:
            self.disc = 1
        if idartist and self.album and self.title and (self.number is not None):
            self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + str(self.number) + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_flac')
        else:
            if idartist and self.album and self.title:
                self.id = base64.b64encode((_force_unicode(idartist, 'utf-8') + _force_unicode(self.album, 'utf-8') + _force_unicode(self.title, 'utf-8')).encode('utf-8') + '_flac')
        self.modified = os.path.getmtime(os.path.split(path)[0]) * 1000
        self.type = 'mp4'
    def time(self):
        return self.duration



def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def ums(i, ignoreZero=True):
    i = int(i)
    hours = i / 3600
    rest = i % 3600
    minutes = rest / 60
    seconds = rest % 60
    if (hours < 10):
        hours = "0" + str(hours)
    if (minutes < 10):
        minutes = "0" + str(minutes)
    if (seconds < 10):
        seconds = "0" + str(seconds)
    if (ignoreZero):
        if (hours == "00"):
            hours = ""
        else:
            hours = hours + ":"
    else:
        hours = hours + ":"
    return hours + str(minutes) + ":" + str(seconds)
def totals():
    return "{ \"totals\" : { \"artists\":" + str(totalArtist) + ", \"albums\":" + str(totalAlbums) + ", \"tracks\":" + str(nrScanned) + ", \"playingTime\":" + str(totalTime) + ", \"timestamp\":" + str(int(time.time())) +  "}, \"Type\":\"totals\"}"
def _force_unicode(bstr, encoding, fallback_encodings=None):
    # We got unicode, we give unicode
    if isinstance(bstr, unicode):
        return bstr

    if fallback_encodings is None:
        fallback_encodings = ['UTF-16', 'UTF-8', 'ISO-8859-1']

    encodings = [encoding] + fallback_encodings

    for enc in encodings:
        try:
            return bstr.decode(enc)
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass

    # Finally, force the unicode
    return bstr.decode(encoding, 'ignore')

def parseFile(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    song = eyed3.load(filename)
    if song is not None:
        if song.tag is not None:
            track = Track(song, filename)
            nrScanned = nrScanned + 1
            perc = int((float(float(nrScanned) / float(countfiles))) * 100)
            p.seek(0)
            p.write(str(perc))
            p.truncate()
            if (countfiles > 100 and nrScanned % int(countfiles/100) == 0 and showInfo):
                inc = time.time()
                #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
                diff = inc-start
                if (perc > 0):
                    tot = (diff / perc) * 100
                    eta = tot - diff
                    sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                    sys.stdout.flush()
            jsonFile.append(json.dumps(track.__dict__,sort_keys=True, indent=2))

def parseMP3(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    song = MP3(filename)
    if song is not None:
        track = MP3Track(song, filename)
        nrScanned = nrScanned + 1
        perc = int((float(float(nrScanned) / float(countfiles))) * 100)
        p.seek(0)
        p.write(str(perc))
        p.truncate()
        if (countfiles > 100 and nrScanned % int(countfiles/100) == 0 and showInfo):
            inc = time.time()
            #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
            diff = inc-start
            if (perc > 0):
                tot = (diff / perc) * 100
                eta = tot - diff
                sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                sys.stdout.flush()
        jsonFile.append(json.dumps(track.__dict__,sort_keys=True, indent=2))

def parseFlac(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    song = FLAC(filename)
    if song is not None:
        track = FlacTrack(song, filename)
        nrScanned = nrScanned + 1
        perc = int((float(float(nrScanned) / float(countfiles))) * 100)
        p.seek(0)
        p.write(str(perc))
        p.truncate()
        if (countfiles > 100 and nrScanned % int(countfiles/100) == 0 and showInfo):
            inc = time.time()
            #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
            diff = inc-start
            if (perc > 0):
                tot = (diff / perc) * 100
                eta = tot - diff
                sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                sys.stdout.flush()
        jsonFile.append(json.dumps(track.__dict__,sort_keys=True, indent=2))

def parseM4A(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    song = MP4(filename)
    if song is not None:
        track = MP4Track(song, filename)
        nrScanned = nrScanned + 1
        perc = int((float(float(nrScanned) / float(countfiles))) * 100)
        p.seek(0)
        p.write(str(perc))
        p.truncate()
        if (countfiles > 100 and nrScanned % int(countfiles/100) == 0 and showInfo):
            inc = time.time()
            #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
            diff = inc-start
            if (perc > 0):
                tot = (diff / perc) * 100
                eta = tot - diff
                sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                sys.stdout.flush()
        jsonFile.append(json.dumps(track.__dict__,sort_keys=True, indent=2))

allfiles = find_files(rootpath, '*.mp3')
allfilesflac = find_files(rootpath, '*.flac')
allfilesm4a = find_files(rootpath, '*.m4a')
countfiles = sum(1 for e in allfiles)
countfiles += sum(1 for e in allfilesflac)
countfiles += sum(1 for e in allfilesm4a)

print "Starting scan for {0} media files in '{1}'".format(countfiles, rootpath)
for filename in find_files(rootpath, '*.mp3'):
    # parseFile(filename, jsonFile)
    parseMP3(filename, jsonFile)

for filename in find_files(rootpath, '*.flac'):
    parseFlac(filename, jsonFile)

for filename in find_files(rootpath, '*.m4a'):
    parseM4A(filename, jsonFile)


f.write("[" + ",\n".join(jsonFile) + "]")
f.close()
p.seek(0)
p.write("100")
p.truncate()
p.close()
inc = time.time()
print "Done scanning, time taken: {0}".format(ums(inc-start, False))
