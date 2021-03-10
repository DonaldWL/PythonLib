'''
Created:   Feb 21, 2021
Author:    Donald W. Long (Donald.W.Long@gmail.com)
-----------------------------------------------------------------------------
CopyRight:

    Copyright (C) 2020-2021  Donald W. Long (Donald.W.Long@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
Description:

  This module contains functions that help you with strings.  Some are
  just wrappers around normal python code.  It just helps to have a function
  with a name that matches what it does.

  For further details see the help file for this module.
-----------------------------------------------------------------------------
Update History:
  Feb 21, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

from collections import namedtuple

  # Is what is returned from SMS._Strings.GetString.  OutCome is the
  # outcome of the operation, True is ok False is not.  CharConsumed is
  # the number of characters consumed, and String, is the string that was
  # removed from the line
_GetStringDef = namedtuple('GetString', ['OutCome', 'CharConsumed', 'String'])


def GetString(Line, QuoteChars = "\"'"):
  '''
  Process a line to extract a string.

  _GetStringDef = GetString(Line, QuoteChars = "\"'")
    _GetStringDef = namedtuple('GetString', ['OutCome', 'CharConsumed', 'String'])
      Is what is returned from SMS._Strings.GetString.  OutCome is the
      outcome of the operation, True is ok False is not.  CharConsumed is
      the number of characters consumed, and String, is the string that was
      removed from the line
    Line = string
      Is the line to process, assumes the first character is the
      start of the string i.e., starts with quote.  It will
      handle the backslash character.
    QuoteChars = String
      Is a list of the characters that can be used for quote.  The default is
      a single quote and the double quote.  Like python's string.
  '''
  TheString = ''

  offset = 1
  _LineLen = len(Line)
  QuoteChar = None
  if _LineLen > 1 and Line[0] in QuoteChars: 
    QuoteChar = Line[0]
    while offset < _LineLen:
      if Line[offset] == '\\':
        offset += 1
        try:
          TheString += Line[offset]
        except IndexError:
          break
      elif Line[offset] in QuoteChar:
        return _GetStringDef(True, offset + 1, TheString)
      else:
        TheString += Line[offset]
      offset += 1

  return _GetStringDef(False, 0, '')  # Invalid string return


def SkipWhiteSpace(String, WhiteSpace = ' \t'):
  '''
  Skip spaces in a line.  and returned the number of
  characters consumed.  This allows you to go thru
  a string one char at a time and skip over the whitespace.

  consumedCharCnt = SkipWhiteSpace(String, WhiteSpace)
    consumedCharCnt
      Is the number of spaces consumed
    String
      String to scan for white space
    WhiteSpace
      Is a list of characters to use for while space.
      The default is a space and tab.
  '''
  try:
    return next(i for i, j in enumerate(String) if j not in WhiteSpace)
  except StopIteration:
    return len(String)
