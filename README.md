scanner.py
==========

A generic mp3 scanner written in python.
The output is a JSON file which can be used to display the collection. One of the possible programs that can use this JSON is [JSMusicDB](https://github.com/lucienimmink/JSMusicDB)
The aim of this program is to be as fast as possible; so no incremental updates are available.

There are just 2 lines you need to alter:
```python
rootpath = r"/volume1/music/"
f = codecs.open('/volume1/web/music/music.json', 'w', "utf-8")
```