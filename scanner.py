#!/usr/bin/env python
# -*- coding: utf8 -*-
""" This program is made possible by the awesome python knowledge of my darling Ivana <3 for ever """

import os, fnmatch, json, sys, codecs, time, eyed3

rootpath = r"/volume1/music/"
#rootpath = r"C:\\Users\\lucien\\Dropbox\\addasoft\\Workspace\\testmusic"
#rootpath = r"d:\\music"
artists = dict()
albums = dict()
jsonFile = list()
f = codecs.open('/volume1/web/music/music.json', 'w', "utf-8")
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
        return u"{\"Naam\":\"" + self.Artiest + "\",\"Titel\":\"\",\"Artiest\":\"\",\"Album\":\"\",\"Track\":null,\"Jaar\":null}"
    
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
        return u"{\"Naam\":\"" + self.Artiest + " - " + self.Album + "\",\"Titel\":\"\",\"Artiest\":\""+self.Artiest+"\",\"Album\":\""+self.Album+"\",\"Track\":null,\"Jaar\":\""+self.Jaar+"\"}"
    
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
        return u"{\"Pad\":\"" + self.Pad + "\",\"Titel\":\"" + self.Titel + "\",\"Artiest\":\""+self.Artiest+"\",\"Album\":\""+self.Album+"\",\"Track\":\""+self.Track+"\",\"Jaar\":\""+self.Jaar+"\",\"U:M:S\":\""+self.Duur+"\",\"Disk\":\""+self.Disk+"\"}"
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
    return "{ \"totals\" : { \"artists\":" + str(totalArtist) + ", \"albums\":" + str(totalAlbums) + ", \"tracks\":" + str(nrScanned) + ", \"playingTime\":" + str(totalTime) + ", \"timestamp\":" + str(int(time.time())) +  "}}" 
def _force_unicode(bstr, encoding, fallback_encodings=None):
    """Force unicode, ignore unknown.
    
    Forces the given string to unicode with first guessing, then forcing by
    using given encoding and ignoring unknown characters. This is sadly many
    times necessary, since there usually are only pieces of string without 
    proper encoding, such as file system file names where usually any bytes
    are accepted as filenames.
    
    :param bstr: String
    :type bstr: Basestring
    
    :param encoding: Assumed encoding, notice that by giving encoding that can
        decode all 8-bit characters such as ISO-8859-1 you effectively may be
        decoding all string regardless were they in that encoding or not.
    :type encoding: string
    
    :param fallback_encodings: Fallback on trying these encodings if not the
        assumed encoding.
    :type fallback_encodings: list of string
    
    :return: Unicoded given string
    :rtype: unicode string
    
    """
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

allfiles = find_files(rootpath, '*.mp3')
countfiles = sum(1 for e in allfiles)
print "Starting scan for",countfiles,"mp3 files in '" + rootpath + "'"
for filename in find_files(rootpath, '*.mp3'):
    
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
            if (countfiles > 100 and nrScanned % int(countfiles/100) == 0):
                inc = time.time()
                #print "Scanner has scanned" , str(nrScanned) , "files, time elapsed =", ums(inc-start)
                diff = inc-start
                if (perc > 0):
                    tot = (diff / perc) * 100
                    eta = tot - diff
                    sys.stdout.write("" + str(perc) + "% done, ETA: " +  ums(eta, False) + "\r")
                    sys.stdout.flush()
            jsonFile.append(track.toString())
jsonFile.append(totals())    
f.write("[" + ",\n".join(jsonFile) + "]")
f.close()
inc = time.time()
print "Done scanning, time taken:", ums(inc-start, False)
