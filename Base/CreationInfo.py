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

  You inherit this class to get information about your instance.  See the
  class for details.
  
  For further details see the help file for this module.
-----------------------------------------------------------------------------
Required Libraries:

  From Python
    traceback
-----------------------------------------------------------------------------
Update History:
  Feb 21, 2021 - Donald W. Long (Donald.W.Long@gmail.com)
    Released
-----------------------------------------------------------------------------
'''

import traceback


class InstanceCreationError(Exception):
  '''
  Is raised when you can not get the information about the instance
  of the class.  This should never happen, but coded up for protection.
  '''


class CCreationInfo(object):
  '''
  Inherit this class to store information about your instance.  This is
  not an abstract class, thus if you just wish info on your module create
  and instance of this.
  
  Available Properties:
  
    ClassName
      Name of the class that was created
      
    CreationFile
      File the class was in
      
    CreationModule
      Module the class was in
      
    InstanceName
      Name of the instance

  Exceptions:
    InstanceCreationError
      Is raised if we cannot access the frame information to get
      the required properties of the class instance.
  '''
  def __init__(self):

    # Loop thru the stack
    frameData = None  # (frame, line)
    for frameData in traceback.walk_stack(None):
      varnames = frameData[0].f_code.co_varnames

        # if the frame is inside a method of this instance,
        # the first argument usually contains either the instance or
        # its class we want to find the first frame, where this is not the case
      if not varnames:
        break  # pragma: no cover
      if frameData[0].f_locals[varnames[0]] not in (self, self.__class__):
        break
    else:
      raise InstanceCreationError("No suitable outer frame found.")  # pragma: no cover

    self._ClassName = self.__class__.__name__

      # [0] CreationFIle
      # [1] CreationLine
      # [2] CreationFunction
      # [3] CreationText
    x = traceback.extract_stack(frameData[0], 1)[0]
    self._CreationFile = x[0]
    self._CreationModule = frameData[0].f_globals["__name__"]
    self._InstanceName = x[3].split("=")[0].strip()
    super().__init__()

    #--------------------------------------------------------------------------
  @property
  def ClassName(self):
    '''
    Property that is the name of the class that was used
    to create this instance
    '''
    return self._ClassName

    #--------------------------------------------------------------------------
  @property
  def CreationFile(self):
    '''
    Property that is the name of the file that the instance
    was created in.
    '''
    return self._CreationFile

    #--------------------------------------------------------------------------
  @property
  def CreationModule(self):
    '''
    Property that is the name of the module that the instance
    was created in.
    '''
    return self._CreationModule

    #--------------------------------------------------------------------------
  @property
  def InstanceName(self):
    '''
    Property that is the name of this instance.
    '''
    return self._InstanceName
