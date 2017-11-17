#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This program is made possible by the awesome python knowledge of my darling Ivana <3 for ever"""

import os, fnmatch, json, sys, codecs, time, argparse, logging, base64
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp3 import EasyMP3 as MP3
from mutagen._util import MutagenError

import scanner.FlacTrack as FlacTrack
import scanner.Mp3Track as Mp3Track
import scanner.Mp4Track as Mp4Track

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

def parseMP3(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    try:
        song = MP3(filename)
        if song is not None:
            track = Mp3Track.Track(song, filename, rootpath)
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
    except MutagenError:
        print "Error occured"


def parseFlac(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    try:
        song = FLAC(filename)
        if song is not None:
            track = FlacTrack.Track(song, filename, rootpath)
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
    except MutagenError:
        print "Error occured"

def parseM4A(filename, jsonFile, showInfo=True):
    global artists
    global albums
    global totalArtist
    global totalAlbums
    global totalTime
    global nrScanned

    try:
        song = MP4(filename)
        if song is not None:
            track = Mp4Track.Track(song, filename, rootpath)
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
    except MutagenError:
        print "Error occured"

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
