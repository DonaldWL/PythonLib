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

  This module allows you to capture how long it takes for a set of python 
  statements to execute.  For details see each class documentation.

  For further details see the help file for this module.
-----------------------------------------------------------------------------
Required Libraries:

  From Python
    timeit
    
  From Libs
    Libs.Base.Converters
-----------------------------------------------------------------------------
Update History:
  Feb 21, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

import timeit

from .Converters import ConvertMillisecondsDays

  #--------------------------------------------------------------------------
class CCaptureTimer(object):
  '''
  CCaptureTimer()
    Used to capture the timer information from CCodeTimer.  CCodeTimer
    will fill in all the data that needs to be captures and then it
    will call the method 'Save'.

    The '__str__' has been overriding to print out the data using 
    Libs.Converters.ConvertMillisecondsDays.

    Methods:
    
      Save
        Is called by the class 'CCodeTimer'.  This is an empty method,
        you must override this method if you wish it to do something.
        
    Saved Data:
      This is the data that CCodeTimer saves in this class for you.  No
      setter's or getter's are used, this is direct access.

      Name  = Is the name that you passed into CCodeTimer.
      Start = Is when the timer started. Comes from timeit.default_timer()
      End   = Is when the timer ended. Comes from timeit.default_timer()
      Took  = How many milliseconds it took.  This is a float, so you can
              have less then a millisecond.
  '''
  def __init__(self):
    self.Name = None
    self.Start = 0
    self.End = 0
    self.Took = 0

    #--------------------------------------------------------------------------
  def Save(self):
    '''
    Allows you save the results to a file or database or what every you
    wish.  If you do not override this method, you can still get the 
    data from variables.
    '''
    pass  # pylint: disable=unnecessary-pass

    #--------------------------------------------------------------------------
  def __str__(self):
    Result = ConvertMillisecondsDays(self.Took)
    FormatString = 'Code Block "{Name}" took: {Days}d {Hours}h {Minutes}m {Seconds}s {Milliseconds}ms'
    return FormatString.format(Name = self.Name,
                               Days = Result.days,
                               Hours = Result.hours,
                               Minutes = Result.minutes,
                               Seconds = Result.seconds,
                               Milliseconds = Result.milliseconds)
    
  #--------------------------------------------------------------------------
class CCodeTimer(object):
  '''
    Used to capture how long a block of code takes to execute.  This 
    class can be used stand alone or with the 'CCaptureTimer' class.
    The 'CCaptureTimer' just allows you to capture data without 
    writing any code.  You can overload this class and do anything
    you wish and not have to use 'CCaptureTimer'.  When this class
    is deleted it will call 'Save'.  If 'CCaptureTimer' is passed
    in it will call the 'CCaptureTimer' "Save'.
    
    The '__str__' has been overriding to return a simple line of
    how long it took.
    
    Methods:
    
      EndTimer
      Save

    Saved Data:
      This is the data that CCodeTimer saves in this class for you.  No
      setter's or getter's are used, this is direct access.

      Name         = Is the name that you passed into CCodeTimer, if not set
                     will be an empty string.
      Start        = Is when the timer started. Comes from timeit.default_timer()
      End          = Is when the timer ended. Comes from timeit.default_timer()
      Took         = How many milliseconds it took.  This is a float, so you can
                     have less then a millisecond.
      CaptureTimer = If not None is the 'CCaptureTimer' you passed in.
  
  Exceptions:
    AttributeError
      Name must be an instance of 'str' or None
      CaptureTimer must be an instance of 'CCaptureTimer' or None
  '''
  def __init__(self, Name = None, CaptureTimer = None):
    self.Name = Name if Name else ''

    if Name and not isinstance(Name, str):
      raise AttributeError("Name must be an instance of str or None")
    
    if CaptureTimer and not isinstance(CaptureTimer, CCaptureTimer):
      raise AttributeError("CaptureTimer must be an instance of CCaptureTimer or None")
    self.CaptureTimer = CaptureTimer

      # Set _Start, just in case we are created without using the 'with' statement.
    self._Start = timeit.default_timer()
    self.End = None
    self._Took = 0

    #--------------------------------------------------------------------------
  def Save(self):
    '''
    This is used to save the data.  Its default behavior is to just print out
    a string using the '__str__' of the class.  You can override this to capture
    the data or print it out in your format.
    '''
    print(str(self))

    #--------------------------------------------------------------------------
  def EndTimer(self):
    '''
    Used to End the timer.  If you use this method to end the timer and not
    the delete method then 'Save' will not be called.  If you have set 
    'CCaptureTimer' then its 'Save' will be called.
    '''
    if not self.End:
      self.End = timeit.default_timer()
      self._Took = (self.End - self._Start) * 1000.0
      if self.CaptureTimer:
        self.CaptureTimer.Name = self.Name
        self.CaptureTimer.Start = self._Start
        self.CaptureTimer.End = self.End
        self.CaptureTimer.Took = self._Took
        self.CaptureTimer.Save()
    
    #--------------------------------------------------------------------------
  def __enter__(self):
    self._Start = timeit.default_timer()
    return self

    #--------------------------------------------------------------------------
  def __exit__(self, exc_type, exc_val, exc_tb):
    if not self.End:
      self.End = timeit.default_timer()
      self._Took = (self.End - self._Start) * 1000.0
      if self.CaptureTimer:
        self.CaptureTimer.Name = self.Name
        self.CaptureTimer.Start = self._Start
        self.CaptureTimer.End = self.End
        self.CaptureTimer.Took = self._Took
        self.CaptureTimer.Save()
      else:
        self.Save()
    
    #--------------------------------------------------------------------------
  def __del__(self):
    if not self.End:
      self.End = timeit.default_timer()
      self._Took = (self.End - self._Start) * 1000.0
      if self.CaptureTimer:
        self.CaptureTimer.Name = self.Name
        self.CaptureTimer.Start = self._Start
        self.CaptureTimer.End = self.End
        self.CaptureTimer.Took = self._Took
        self.CaptureTimer.Save()
      else:
        self.Save()

    #--------------------------------------------------------------------------
  def __str__(self):
    return 'Code Block: ' + self.Name + ' Took: ' + str(self._Took) + 'ms'
  