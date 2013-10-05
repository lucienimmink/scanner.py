# -*- coding: utf-8 -*-
################################################################################
#  Copyright (C) 2013  Travis Shirk <travis@pobox.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
################################################################################
'''
Compatibility for various versions of Python (e.g. 2.6, 2.7, and 3.3)
'''
import sys
import types


PY2 = sys.version_info[0] == 2

if PY2:
    StringTypes = types.StringTypes
    UnicodeType = unicode
    BytesType = str
    unicode = unicode

    from ConfigParser import SafeConfigParser as ConfigParser
    from ConfigParser import Error as ConfigParserError

    from StringIO import StringIO
else:
    StringTypes = (str,)
    UnicodeType = str
    BytesType = bytes
    unicode = str

    from configparser import ConfigParser
    from configparser import Error as ConfigParserError

    from io import StringIO


def toByteString(n):
    if PY2:
        return chr(n)
    else:
        return bytes((n,))


def byteiter(bites):
    assert(isinstance(bites, str if PY2 else bytes))
    for b in bites:
        yield b if PY2 else bytes((b,))
