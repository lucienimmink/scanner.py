#!/usr/bin/env python
# -*- coding: utf8 -*-
"""This program is made possible by the awesome python knowledge of my darling Ivana <3 for ever"""

import os, fnmatch, json, sys, codecs, time, argparse, logging
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp3 import EasyMP3 as MP3
from mutagen._util import MutagenError
import scanner._utils as utils
import scanner.FlacTrack as FlacTrack
import scanner.Mp3Track as Mp3Track
import scanner.Mp4Track as Mp4Track

parser = argparse.ArgumentParser(
    description=
    'Scans a given directory for MP3\'s and places the output file in an optional directory'
)
parser.add_argument('scanpath', metavar='scanpath', help='directory to scan')
parser.add_argument(
    '--destpath',
    metavar='destination path',
    help='directory to place the output json in')
parser.add_argument('--stdout', metavar='stdout', help='print status to stdout or not')
args = parser.parse_args()

rootpath = args.scanpath
destpath = args.destpath or args.scanpath
showInfo = args.stdout == 'True'

""" logging """
logging.basicConfig(filename='scanner.log', level=logging.DEBUG)

f = codecs.open(destpath + '/node-music.json', 'w', "utf-8")
p = codecs.open(destpath + '/progress.txt', 'w', "utf-8")

jsonFile = list()
nrScanned = 0
start = time.time()


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                yield os.path.join(root, basename)


def updateInfo():
    global nrScanned
    global showInfo

    nrScanned = nrScanned + 1
    perc = int((float(float(nrScanned) / float(countfiles))) * 100)
    p.seek(0)
    p.write(str(perc))
    p.truncate()
    if (countfiles > 100 and nrScanned % int(countfiles / 100) == 0
            and showInfo):
        inc = time.time()
        diff = inc - start
        if (perc > 0):
            tot = (diff / perc) * 100
            eta = tot - diff
            sys.stdout.write("" + str(perc) + "% done, ETA: " +
                             utils.ums(eta, False) + "\r")
            sys.stdout.flush()


def parseMP3(filename):
    global jsonFile
    try:
        song = MP3(filename)
        if song is not None:
            track = Mp3Track.Track(song, filename, rootpath)
            updateInfo()
            jsonFile.append(
                json.dumps(track.__dict__, sort_keys=True, indent=2))
    except MutagenError:
        print "Error occured"


def parseFlac(filename):
    global jsonFile
    try:
        song = FLAC(filename)
        if song is not None:
            track = FlacTrack.Track(song, filename, rootpath)
            updateInfo()
            jsonFile.append(
                json.dumps(track.__dict__, sort_keys=True, indent=2))
    except MutagenError:
        print "Error occured"


def parseM4A(filename):
    global jsonFile
    try:
        song = MP4(filename)
        if song is not None:
            track = Mp4Track.Track(song, filename, rootpath)
            updateInfo()
            jsonFile.append(
                json.dumps(track.__dict__, sort_keys=True, indent=2))
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
    parseMP3(filename)

for filename in find_files(rootpath, '*.flac'):
    parseFlac(filename)

for filename in find_files(rootpath, '*.m4a'):
    parseM4A(filename)

f.write("[" + ",\n".join(jsonFile) + "]")
f.close()
p.seek(0)
p.write("100")
p.truncate()
p.close()
end = time.time()
print "Done scanning, time taken: {0}".format(utils.ums(end - start, False))
