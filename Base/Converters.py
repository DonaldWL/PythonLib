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

  This module has functions that will convert data from one format to another.
  See each function for details.
  
  For further details see the help file for this module.
-----------------------------------------------------------------------------
Required Libraries:

  From Python
    from collections import namedtuple
-----------------------------------------------------------------------------
Update History:
  Feb 21, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

from collections import namedtuple

  #--------------------------------------------------------------------------
def ConvertMillisecondsDays(milliseconds):
  '''
    Converts milliseconds all the way to days.  Normally used
    when you are running a timer to see how long something takes.
    This is using namedtupel.  Thus, the values can be accessed
    via index or a name.

    <result> = ConvertMillisecondsDays(<milliseconds>)

      <results>  => namedtuple
        (<days>, <hours>, <minutes>, <seconds>, <milliseconds>)
  '''
  Result = namedtuple('Result', ['days', 'hours', 'minutes', 'seconds', 'milliseconds'])
  seconds = int(((milliseconds / 1000) % 60))
  minutes = int(((milliseconds / (1000 * 60)) % 60))
  hours = int(((milliseconds / (1000 * 60 * 60)) % 24))
  days = int(((milliseconds / (1000 * 60 * 60 * 24))))
  milli = milliseconds - ((seconds * 1000) + (minutes * (60 * 1000)) + 
                          (hours * (1000 * 60 * 60)) + (days * (1000 * 60 * 60 * 24)))

  return Result(days, hours, minutes, seconds, milli)

  #--------------------------------------------------------------------------
def ConvertMillisecondsWeeks(milliseconds):
  '''
  <results> = ConvertMillisecondsWeeks
    Converts milliseconds all the way to weeks.  Normally used
    when you are running a timer to see how long something takes.
    This is using namedtupel.  Thus, the values can be accessed
    via index or a name.

    <result> = ConvertMillisecondsDays(<milliseconds>)

      <results>  => namedtuple
        (<weeks>, <days>, <hours>, <minutes>, <seconds>, <milliseconds>)
  '''
  Result = namedtuple('Result', ['weeks', 'days', 'hours', 'minutes', 'seconds', 'milliseconds'])
  seconds = int(((milliseconds / 1000) % 60))
  minutes = int(((milliseconds / (1000 * 60)) % 60))
  hours = int(((milliseconds / (1000 * 60 * 60)) % 24))
  days = int(((milliseconds / (1000 * 60 * 60 * 24)) % 7))
  weeks = int((milliseconds / (1000 * 60 * 60 * 24 * 7)))
  milli = milliseconds - ((seconds * 1000) + (minutes * (60 * 1000)) + 
                          (hours * (1000 * 60 * 60)) + (days * (1000 * 60 * 60 * 24)) + (weeks * (1000 * 60 * 60 * 24 * 7)))

  return Result(weeks, days, hours, minutes, seconds, milli)
