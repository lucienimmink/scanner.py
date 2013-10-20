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