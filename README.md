scanner.py
==========

A generic mp3 scanner written in python.
The output is a JSON file which can be used to display the collection. One of the possible programs that can use this JSON is [JSMusicDB](https://github.com/lucienimmink/JSMusicDB)
The aim of this program is to be as fast as possible; so no incremental updates are available.

The script will continue to run after the initial scan; it will watch the folder and add the new data in an increment file; Every time the script is rerun the increment file is nullified.

Requirements
------------
- eyeD3: http://eyed3.nicfit.net/
- watchdog: https://pypi.python.org/pypi/watchdog

Please download and install the requirements first before running scanner.py!

Output format
-------------
The output JSON is 1 large array object with 4 types of nodes
- Artist
- Album
- Track
- Totals
Each type has specific attributes with the bare information a parser will need to parse and link the nodes

Artist node
-----------
```javascript
{
    "Naam": "30 Seconds To Mars", 
    "Type": "artist"
}
```
Naam is dutch for name

Album node
----------
```javascript
{
    "Album": "30 Seconds to Mars", 
    "Artiest": "30 Seconds To Mars", 
    "Jaar": "2002-08-27", 
    "Naam": "30 Seconds to Mars", 
    "Type": "album"
}
```
Artiest is dutch for Artist, Jaar is dutch for Year

Track node
----------
```javascript
{
    "Album": "30 Seconds to Mars", 
    "Artiest": "30 Seconds To Mars", 
    "Disk": 1, 
    "Duur": "03:50", 
    "Jaar": "2002-08-27", 
    "Pad": "[xxxx]30 Seconds To Mars - 30 Seconds To Mars - 01 - Capricorn (a Brand New Name).mp3", 
    "Titel": "Capricorn (A Brand New Name)", 
    "Track": 1, 
    "Type": "track", 
    "seconds": 230
}
```
Duur is dutch for length, Pad is dutch for path, Titel is dutch for title. Please use the full path to the file in the Pad attribute

Totals node
-----------
```javascript
{ "totals" : { "artists":10, "albums":26, "tracks":291, "playingTime":73732, "timestamp":1382273323}, "Type":"totals"}
```
Instead of calculating the totals in the front-end; please calculate them in your scanner, since this is a one time only process. playingTime is in seconds, timestamp is EPOCH