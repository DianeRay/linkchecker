# -*- coding: iso-8859-1 -*-
"""various string utils"""
# Copyright (C) 2000-2004  Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import re
import sys

markup_re = re.compile("<.*?>", re.DOTALL)

SQLTable = [
    ("'","''")
]


def stripQuotes (s):
    "Strip optional quotes"
    if len(s)<2:
        return s
    if s[0]=="\"" or s[0]=="'":
        s = s[1:]
    if s[-1]=="\"" or s[-1]=="'":
        s = s[:-1]
    return s


def indent (s, level):
    "indent each line of s with <level> spaces"
    return indentWith(s, level * " ")


def indentWith (s, indent):
    "indent each line of s with given indent argument"
    i = 0
    while i < len(s):
        if s[i]=="\n" and (i+1) < len(s):
            s = s[0:(i+1)] + indent + s[(i+1):]
        i += 1
    return s


def blocktext (s, width):
    "Adjust lines of s to be not wider than width"
    # split into lines
    s = s.split("\n")
    s.reverse()
    line = None
    ret = ""
    while len(s):
        if line:
            line += "\n"+s.pop()
        else:
            line = s.pop()
        while len(line) > width:
            i = getLastWordBoundary(line, width)
            ret += line[0:i].strip() + "\n"
            line = line[i:].strip()
    return ret + line


def getLastWordBoundary (s, width):
    """Get maximal index i of a whitespace char in s with 0 < i < width.
    Note: if s contains no whitespace this returns width-1"""
    match = re.compile(".*\s").match(s[0:width])
    if match:
        return match.end()
    return width-1


def getLineNumber (s, index):
    "return the line number of str[index]"
    i=0
    if index<0: index=0
    line=1
    while i<index:
        if s[i]=='\n':
            line += 1
        i += 1
    return line


def paginate (text, lines=22):
    """print text in pages of lines size"""
    textlines = text.split("\n")
    curline = 1
    for line in textlines:
        print line
        curline += 1
        if curline >= lines and sys.stdin.isatty():
            curline = 1
            print "press return to continue..."
            sys.stdin.read(1)


def remove_markup (s):
    mo = markup_re.search(s)
    while mo:
        s = s[0:mo.start()] + s[mo.end():]
        mo = markup_re.search(s)
    return s


def unquote (s):
    if not s:
        return ''
    return stripQuotes(s)


def strsize (b):
    """return human representation of bytes b"""
    if b<1024:
        return "%d Byte"%b
    b /= 1024.0
    if b<1024:
        return "%.2f kB"%b
    b /= 1024.0
    if b<1024:
        return "%.2f MB"%b
    b /= 1024.0
    return "%.2f GB"

