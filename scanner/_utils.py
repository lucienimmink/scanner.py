#!/usr/bin/env python
# -*- coding: utf8 -*-


class Time:
    def ums(i, ignoreZero=True):
        i = float(i)
        hours = int(i / 3600)
        rest = i % 3600
        minutes = int(rest / 60)
        seconds = int(rest % 60)
        if hours < 10:
            hours = "0" + str(hours)
        if minutes < 10:
            minutes = "0" + str(minutes)
        if seconds < 10:
            seconds = "0" + str(seconds)
        if ignoreZero:
            if hours == "00":
                hours = ""
            else:
                hours = hours + ":"
        else:
            hours = hours + ":"
        return hours + str(minutes) + ":" + str(seconds)


class force_unicode:
    def force_unicode(bstr, encoding, fallback_encodings=None):
        # We got unicode, we give unicode
        return bstr
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
