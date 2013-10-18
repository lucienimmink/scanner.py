#!/usr/bin/env python
# -*- coding: utf8 -*-
""" This program is made possible by the awesome python knowledge of my darling Ivana <3 for ever """

import os, fnmatch, json, sys, codecs, time, eyed3, argparse, logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.events import LoggingEventHandler

parser = argparse.ArgumentParser(description='Scans a given directory for MP3\'s and places the output file in an optional directory');
parser.add_argument('scanpath', metavar='scanpath', help='directory to scan')
parser.add_argument('--destpath', metavar='destination path', help='directory to place the output json in')
args = parser.parse_args()

rootpath = args.scanpath
destpath = args.destpath or args.scanpath

class my_handler(FileSystemEventHandler): 
    def __init__(self): 
        FileSystemEventHandler.__init__(self) 

    def on_any_event(self, event): 
        if type(event) == FileModifiedEvent:
            # file modified (added or updated)
            if (event.src_path.find(".mp3") ):
                time.sleep(0.1)
                parseFile(event.src_path, increment, False)
                inc = codecs.open(destpath + '/increment.json', 'w', "utf-8")
                increment.append("{\"ts\":" + str(int(time.time()))  + ", \"Type\": \"ts\"}");
                inc.write("[" + ",\n".join(increment) + "]")
                inc.close()


""" logging """
logging.basicConfig(filename='scanner.log', level=logging.DEBUG)

f = codecs.open(destpath + '/music.json', 'w', "utf-8")
inc = codecs.open(destpath + '/increment.json', 'w', "utf-8")
inc.close()

artists = dict()
albums = dict()
jsonFile = list()
increment = list()
nrScanned = 0
total_files = 0
totalArtist = 0
totalAlbums = 0
totalTime = 0
start = time.time()

class Artist:
    def __init__ (self, file):
        if (file.tag.artist):
            self.Artiest = file.tag.artist.replace("\"", "")
        else:
            self.Artiest = ""
    def toString (self):
        return u"{\"Naam\":\"" + self.Artiest + "\",\"Titel\":\"\",\"Artiest\":\"\",\"Album\":\"\",\"Track\":null,\"Jaar\":null, \"Type\":\"artist\"}"
    
class Album:
    def __init__ (self, file):
        if (file.tag.artist):
            self.Artiest = file.tag.artist.replace("\"", "")
        else:
            self.Artiest = ""
        if (file.tag.album):
            self.Album = file.tag.album.replace("\"", "")
        else:
            self.Album = ""
        if file.tag.best_release_date:
            self.Jaar = str(file.tag.best_release_date)
        else:
            self.Jaar = "null"
    def toString (self):
        return u"{\"Naam\":\"" + self.Artiest + " - " + self.Album + "\",\"Titel\":\"\",\"Artiest\":\""+self.Artiest+"\",\"Album\":\""+self.Album+"\",\"Track\":null,\"Jaar\":\""+self.Jaar+"\", \"Type\":\"album\"}"
    
class Track:
    def __init__ (self, file, path):
        if file.tag.artist:
            self.Artiest = file.tag.artist.replace("\"", "")
        else:
            self.Artiest = ""
        if file.tag.album:
            self.Album = file.tag.album.replace("\"", "")
        else:
            self.Album = ""
        if file.tag.best_release_date:
            self.Jaar = str(file.tag.best_release_date)
        else:
            self.Jaar = "null"
        self.Track = str(file.tag.track_num[0])
        if file.tag.title:
            self.Titel = file.tag.title.replace("\"", "")
        else:
            self.Titel = ""
        if file.info.time_secs:
            self.Duur = ums(file.info.time_secs)
            self.seconds = file.info.time_secs
        else:
            self.Duur = ""
            self.seconds = 0
        self.Pad = _force_unicode(path, "utf-8").replace("\\", "\\\\")
        if file.tag.disc_num:
            self.Disk = str(file.tag.disc_num[0])
        else:
            self.Disk = ""
        
        
    def toString (self):
        return u"{\"Pad\":\"" + self.Pad + "\",\"Titel\":\"" + self.Titel + "\",\"Artiest\":\""+self.Artiest+"\",\"Album\":\""+self.Album+"\",\"Track\":\""+self.Track+"\",\"Jaar\":\""+self.Jaar+"\",\"U:M:S\":\""+self.Duur+"\",\"Disk\":\""+self.Disk+"\", \"Type\":\"track\"}"
    def time(self):
        return self.seconds

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
            if song.tag.artist not in artists:
                artist = Artist(song)
                jsonFile.append(artist.toString())
                artists[song.tag.artist] = True
                totalArtist = totalArtist + 1
            combined = song.tag.album
            if song.tag.artist:
                if combined:
                    combined = song.tag.artist + combined
                else:
                    combined = song.tag.artist
            if combined not in albums:
                album = Album(song)
                jsonFile.append(album.toString())
                albums[combined] = True
                totalAlbums = totalAlbums + 1
            track = Track(song, filename)
            totalTime = totalTime + track.seconds
            nrScanned = nrScanned + 1
            perc = int((float(float(nrScanned) / float(countfiles))) * 100)
            if (countfiles > 100 and nrScanned % int(countfiles/100) == 0 and showInfo):
                inc = time.time()
                #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
                diff = inc-start
                if (perc > 0):
                    tot = (diff / perc) * 100
                    eta = tot - diff
                    sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                    sys.stdout.flush()
            jsonFile.append(track.toString())


allfiles = find_files(rootpath, '*.mp3')
countfiles = sum(1 for e in allfiles)
print "Starting scan for",countfiles,"mp3 files in '" + rootpath + "'"
logging.info("Starting scan for",countfiles,"mp3 files in '" + rootpath + "'")
for filename in find_files(rootpath, '*.mp3'):
    parseFile(filename, jsonFile)
jsonFile.append(totals())    
f.write("[" + ",\n".join(jsonFile) + "]")
f.close()
inc = time.time()
print "Done scanning, time taken:", ums(inc-start, False)
logging.info("Done scanning, time taken:", ums(inc-start, False))

# continue scanning for new files; place them in the incremental file
event_handler = my_handler()
observer = Observer()
observer.schedule(event_handler, path=rootpath, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()