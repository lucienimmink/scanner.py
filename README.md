# scanner.py

A generic mp3 scanner written in python3.
The output is a JSON file which can be used to display the collection. One of the possible programs that can use this JSON is [JSMusicDB](https://github.com/lucienimmink/JSMusicDB)
The aim of this program is to be as fast as possible; so no incremental updates are available.

The script will continue to run after the initial scan; it will watch the folder and add the new data in an increment file; Every time the script is rerun the increment file is nullified.

## Output format

The output JSON is 1 array with objects holding the track info

## Track node

```javascript
{
  "album": "Adrenaline Mob",
  "albumartist": null,
  "artist": "Adrenaline Mob",
  "disc": null,
  "duration": 278000,
  "id": "QWRyZW5hbGluZSBNb2JBZHJlbmFsaW5lIE1vYjFQc3ljaG9zYW5l",
  "modified": 1477837993913.5518,
  "number": 1,
  "path": "Adrenaline Mob/Adrenaline Mob - Adrenaline Mob EP/Adrenaline Mob - Adrenaline Mob EP - 01 - Psychosane.mp3",
  "title": "Psychosane",
  "year": "2011",
  "type": "mp3"
}
```
