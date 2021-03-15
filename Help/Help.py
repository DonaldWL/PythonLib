'''
Created:   Feb 9, 2021
Author:    Donald W. Long
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

  Is a simple help system.  It allows you to create help files and then
  dump the help files to an out file as needed.  It is not very complicated.
  See this 'Libs.Help.HelpFiles.HelpFiles.help'.  This will explain how
  to create your text files for help and manage them with this help system.

  If you wish to have your program output the above help file for the help
  system.  You can add the following to your 'HelpDirs'.

    import Libs.Help

      This will get you the following
        CHelp, MYHELPFILEDIR and HelpException

        MYHELPFILEDIR will contain the directory that contains the
        help file for the system.  The help file is called
        '_helpsystem.help'.

  Then when you make an instance of the CHelp call add this to your list
  and update you '_TopicTran.help' with the topic name you wish.  If you
  do not use the topic name of 'helpfiles' then you need to add the topic
  and then a file using 'file:'.  For details on how to create all your
  help fils see the file ._helpsystem.help'.  It is a normal help file
  for this system that can be dumped by an application using the help
  system or you can just read it.  All help files are simple text files.
-----------------------------------------------------------------------------
Exceptions:

  Python Exceptions

    AttributeError
      The passed in attribute is not valid.

  Help Defined Exceptions

    HelpException
      Any error that is not an AttributeError will have this exception.
-----------------------------------------------------------------------------
Update History:
  Date: Feb 9, 2021
    Released
  Date: Mar 14, 2021
    Added support of tags
    General comment cleanup
  Date: Mar 15, 2021
    Added support for python module in help files that contains tags.
-----------------------------------------------------------------------------
'''
import os
import sys
from collections import namedtuple
from enum import IntEnum
import importlib.util


MYHELPFILEDIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/HelpFiles')

  # This is the definition for tags that you wish to have replaced in your help file.
  # You pass in to help 'Tags'.  This is a dictionary with the name of the tag.  Each
  # line in the help file will be scanned for the tag and based on the tag type it
  # will be replaced.  The tag will have the following added around it @@@<tag>@@@.
  # The value of the tag can be a string, tuple, or list.  If a tuple or list then
  # each item is placed in your file, tag type will determine how this is done.
TagInfoDef = namedtuple('TagInfo', ['Type', 'Value'])

  # These are the types for TagInfoDef.
  #   SINGLEWORD
  #     Replaces the tag with the value.  If tuple or list does a ' '.join
  #   SENTENCE
  #     Replaces the tag with the value and adds a new line.  If tuple or 
  #     list does a ' '.join
  #   PARAGRAPH
  #     Replaces the tag with the value and adds new lines for each line.  If
  #     just a string then you get one line, but if tuple or list each item
  #     creates a new line.
class TagTypes(IntEnum):
  SINGLEWORD = 0
  SENTENCE = 1
  PARAGRAPH = 2

class HelpException(Exception):
  pass


class CHelp(object):
  '''
  CHelp(HelpDirs = None, TopicSeperatorLine = None,
        PreTopic = None, PostTopic = None, TopicIndent = 0,
        OutFile = None, Tags = None)

  HelpDirs
    See the setter.
  TopicSeperatorLine
    See the setter.
  PreTopic
    See the setter.
  PostTopic
    See the setter.
  TopicIndent
    See the setter.  Default is 0.
  CopyRight
    See the setter.
  OutFile
    See the setter.
  Tags
    See the setter.
  '''
  def __init__(self, HelpDirs = None, TopicSeperatorLine = None, PreTopic = None, PostTopic = None,
               TopicIndent = 0, CopyRight = None, OutFile = None,Tags = None):
    self._Topics = {}
    self._TopicList = None

    self._OutFile = None
    self.OutFile = OutFile

    self._CopyRight = None
    self.CopyRight = CopyRight

      # Tags must be set before HelpDirs.
    self._Tags = []
    self.Tags = Tags
    
    self._HelpDirs = None
    self.HelpDirs = HelpDirs

    self._TopicSeperatorLine = None
    self.TopicSeperatorLine = TopicSeperatorLine

    self._PreTopic = None
    self.PreTopic = PreTopic

    self._PostTopic = None
    self.PostTopic = PostTopic

    self._TopicIndent = 0
    self.TopicIndent = TopicIndent

    #--------------------------------------------------------------------------
  def Process(self, HelpTopics):
    '''
    Used to process all the passed in help topics.

    Process(HelpTopics)

      HelpTopics
        These are all the topics you wish to process (have written out
        to the OutFile).  Must be a list or tuple of topics.
    '''
    Topics = None
    NumTags = None if self._Tags is None else len(self._Tags)

    if not isinstance(HelpTopics, (list, tuple)):
      raise AttributeError(f'HelpTopics must be a non empty string or list or tuple ({str(type(HelpTopics))})')

    Topics = list(HelpTopics).copy()

    ProcessinFirstTopic = False
    IndentSpaces = ''

    if self._PreTopic is not None:
      Topics.insert(0, self._PreTopic)
      ProcessinFirstTopic = True
    if self._PostTopic is not None:
      Topics.append(self._PostTopic)

    while Topics:
      if not Topics[0] in self._Topics.keys():
        raise HelpException(f'Unable to find topic ({Topics[0]})')

      try:
        if self._PostTopic is not None and len(Topics) == 1:
          IndentSpaces = ''
        elif not ProcessinFirstTopic:
          IndentSpaces = ' ' * self._TopicIndent
        else:
          ProcessinFirstTopic = False
        with open(self._Topics[Topics[0]], 'r') as HelpFile:
          for line in HelpFile:

              # If they have topic lists setup then process the help
              # file looking for the place to put the topic lists.
            if self._TopicList and '@@@HelpTopics' in line:
              xline = line.strip()
              if xline.startswith('@@@HelpTopics') and xline.endswith('@@@'):
                offset = next(i for i, j in enumerate(line) if j not in ' \t')
                xline = xline[13:-4].strip()

                  # Get the width if user supplied it, else 70
                width = 70
                if xline and xline[0] == ',':
                  xline = xline[1:].strip()
                  width = int(xline)
                xIndentSpaces = IndentSpaces + (' ' * offset)
                width = width - len(xIndentSpaces)

                  # Calc the maximum number of names we can put on one line
                lines = ''
                loc = 0
                pad = len(max(self._TopicList, key = len))
                maxNames = int(round(width / (pad + 1)))

                  # Build the lines up.
                while loc < len(self._TopicList):
                  lines = lines + xIndentSpaces
                  for Name in self._TopicList[loc:loc + maxNames]:
                    lines = lines + Name + ' '
                    lines = lines + ' ' * (pad - len(Name))
                  lines = lines + '\n'
                  loc += maxNames

                  # Write all the lines out
                self._OutFile.write(lines)
              else:
                self._OutFile.write(IndentSpaces + line)
            else:
              if NumTags: line = self._ProcessTags(line)
              self._OutFile.write(IndentSpaces + line)

        Topics.pop(0)
      except (OSError, IOError) as err:
        raise HelpException('Unable to open Topic file {0} for Topic {1} ({2})'.format(self._Topics[Topics[0]],
                                                                                       Topics[0],
                                                                                       str(err))) from FileNotFoundError

      if self._TopicSeperatorLine and Topics:
        self._OutFile.write(self._TopicSeperatorLine)

    if self._CopyRight is not None:
      self._OutFile.write(self._CopyRight)

    #--------------------------------------------------------------------------
  @property
  def CopyRight(self):
    '''
    Gets the copy right.
    '''
    return self._CopyRight

    #--------------------------------------------------------------------------
  @CopyRight.setter
  def CopyRight(self, CopyRight):
    '''
    Is a copyright that will be written out after all the topics
    have been written.  If this will only happened if it is not
    None.  Must be None or a string.  No EOL are managed for you.
    '''
    if CopyRight is not None and not isinstance(CopyRight, str):
      raise AttributeError('CopyRight must be None or string ({0})'.format(str(type(CopyRight))))
    self._CopyRight = CopyRight

    #--------------------------------------------------------------------------
  @property
  def HelpDirs(self):
    '''
    Gets the setting of the HelpDirs.
    '''
    return self._HelpDirs

    #--------------------------------------------------------------------------
  @HelpDirs.setter
  def HelpDirs(self, HelpDirs):
    '''
    Is a string, tuple, or list of help directories to look at.
    A string would only be one help directory.  If you pass
    in None then the current directory as the directory 'HelpFiles'
    added on to it and that is assume the location of all your
    help files.

    Has a setter and getter defined, thus you can change these
    between runs without having to create a new instance.
    '''
    self._HelpDirs = []
    xHelpDirs = []
    if HelpDirs is None:
      xHelpDirs.append(os.path.join(os.getcwd(), "HelpFiles"))
    elif isinstance(HelpDirs, str) and HelpDirs.strip():
      xHelpDirs.append(HelpDirs)
    elif isinstance(HelpDirs, (tuple, list)):
      xHelpDirs = list(HelpDirs).copy()
    else:
      raise AttributeError(f'HelpDirs must be a list, tuple, or string ({str(type(HelpDirs))})')
    
    self._Tags = [self._Tags[0]]
    for Dir in xHelpDirs:
      self._HelpDirs.append(os.path.abspath(os.path.expanduser(os.path.expandvars(Dir))))
      if not os.path.exists(self._HelpDirs[-1]):
        raise AttributeError(f'HelpDir {self._HelpDirs[-1]} does not exist')
      if not os.path.isdir(self._HelpDirs[-1]):
        raise AttributeError(f"HelpDir {self._HelpDirs[-1]} is not a directory")
      
      self._LoadTagFile(Dir) # Load tag file if found.

    self._ProcessTopicTran()
    
    #--------------------------------------------------------------------------
  @property
  def OutFile(self):
    '''
    Gets the out file.
    '''
    return self._OutFile

    #--------------------------------------------------------------------------
  @OutFile.setter
  def OutFile(self, OutFile):
    '''
    Is the out file (from open) to write the help text to.  If None
    then will default to 'sys.stdout'.  This could also be your
    own class but must have a method called 'write' that takes
    msg:

      <class>.write(msg)

    No EOL should be written out by write.  The message will contain
    the EOL as needed.  i.e, like print("fun in the sun\n", end = "").

    Has a setter and getter defined, thus you can change these
    between runs without having to create a new instance.
    '''
    if OutFile is None:
      OutFile = sys.stdout
    if not hasattr(OutFile, 'write'):
      raise AttributeError("OutFile does not have an attribute of write")
    self._OutFile = OutFile

    #--------------------------------------------------------------------------
  @property
  def PreTopic(self):
    '''
    Gets the pre topic
    '''
    return self._PreTopic

    #--------------------------------------------------------------------------
  @PreTopic.setter
  def PreTopic(self, PreTopic):
    '''
    If you wish a topic to be written out before all other topics then
    pass this in with the pre topic.  Default is None.
  
    Has a setter and getter defined, thus you can change these
    between runs without having to create a new instance.
    '''
    if PreTopic is None:
      self._PreTopic = None
    elif not isinstance(PreTopic, str):
      raise AttributeError('PreTopic must be None or string ({0})'.format(str(type(PreTopic))))
    else:
      self._PreTopic = PreTopic.strip()

    #--------------------------------------------------------------------------
  @property
  def PostTopic(self):
    '''
    Get the Post topic.
    '''
    return self._PostTopic

    #--------------------------------------------------------------------------
  @PostTopic.setter
  def PostTopic(self, PostTopic):
    '''
    This is just like PreTopic but is written out after all the other
    topics have been processed.

    Has a setter and getter defined, thus you can change these
    between runs without having to create a new instance.
    '''
    if PostTopic is None:
      self._PostTopic = None
    elif not isinstance(PostTopic, str):
      raise AttributeError('PostTopic must be None or string ({0})'.format(str(type(PostTopic))))
    else:
      self._PostTopic = PostTopic.strip()

    #--------------------------------------------------------------------------
  @property
  def Tags(self):
    '''
    Gets the Tags, this is not just the tags you passed in.  It is a list of
    all the tag dictionaries that have been created.  The fist item in the
    list is the tags from you passing in your Tags.  If you passed in None
    it will be and empty dictionary.  If more than one item in the list then
    tags also got loaded from Tags.py from help dirs.  The order of these
    tags matches the HelpDirs order.
    
    Every time you set the HelpDirs the list is reset.  It will always 
    keep your tags as the first item.  If you change your tags then the
    first item will be updated.
    '''
    return self._Tags
  
    #--------------------------------------------------------------------------
  @Tags.setter
  def Tags(self, Tags = None):
    '''
    Is a either None or a dictionary of tags that you wish to have 
    the help system process.  See 'TagInfoDef' and 'TagTypes'.  All types 
    are checked to make sure the dictionary is valid.  Any item in the
    dictionary that is not will raise AttributeError.  If a key name
    is spaces or empty will raise AttributeError.
    '''
    if Tags is None:
      Tags = {}
    else:
      self._ValidateTags(Tags)

    if self._Tags:
      self._Tags[0] = Tags
    else:
      self._Tags.append(Tags)
    
    #--------------------------------------------------------------------------
  @property
  def Topics(self):
    return self._Topics

    #--------------------------------------------------------------------------
  @property
  def TopicIndent(self):
    '''
    Gets the Topic indent.
    '''
    return self._TopicIndent

    #--------------------------------------------------------------------------
  @TopicIndent.setter
  def TopicIndent(self, TopicIndent):
    '''
    Is the how many spaces to indent your help text from the help
    files.  The PreTopic and PostTOpic will not be indented.  This
    allows you to create your help files starting at column one but
    having your PreTopic start at column 1 and other topics indented.
    Must be an integer 0 or greater.
    '''
    if not isinstance(TopicIndent, int) and TopicIndent < 0:
      raise AttributeError('TopicIndent must be a positive integer {0}'.format(str(TopicIndent)))
    self._TopicIndent = TopicIndent

    #--------------------------------------------------------------------------
  @property
  def TopicList(self):
    '''
    If you have t: in your _TopicTran.help file then this will contain all the
    topics with a t:.  If not it will be an empty list.
    '''
    return self._TopicList

    #--------------------------------------------------------------------------
  @property
  def TopicSeperatorLine(self):
    '''
    Gets the Topic Seperator
    '''
    return self._TopicSeperatorLine

    #--------------------------------------------------------------------------
  @TopicSeperatorLine.setter
  def TopicSeperatorLine(self, TopicSeperatorLine = None):
    '''
    This is a string or None.  If the string is not empty it will
    be written out after every topic is processed, except the last
    topic in the list.  Normally you set this to '\n'.  Thus a blank
    line will be written between each topic.  Default is empty string.
    None will also default to empty string.

    Has a setter and getter defined, thus you can change these
    between runs without having to create a new instance.
    '''
    if TopicSeperatorLine is None:
      self._TopicSeperatorLine = ''
    elif not isinstance(TopicSeperatorLine, str):
      raise AttributeError('TopicSeperatorLine must be None or string ({0})'.format(str(type(TopicSeperatorLine))))
    else:
      self._TopicSeperatorLine = TopicSeperatorLine

    #--------------------------------------------------------------------------
  def _ExpandFileName(self, FileName):
    '''
    Expand the passed in FileName.  If it returns None then the filedoes not 
    exist.
    '''
    xFileName = None

    for Dir in self._HelpDirs:
      xFileName = os.path.join(Dir, FileName)
      if os.path.exists(xFileName) and os.path.isfile(xFileName):
        break
      xFileName = None

    return xFileName

    #--------------------------------------------------------------------------
  def _LoadTagFile(self, HelpDIr):
    TagsFile = os.path.abspath(os.path.join(HelpDIr, 'Tags.py'))
    if os.path.exists(TagsFile) and os.path.isfile(TagsFile):
      spec = importlib.util.spec_from_file_location('HelpTags', TagsFile)
      HTags = importlib.util.module_from_spec(spec)
      try:
        spec.loader.exec_module(HTags)
      except (SyntaxError, NameError) as err:
        self._OutFile.write(f"ERROR: {str(err)} in module {TagsFile}")
        return
        
      self._ValidateTags(HTags.Tags)
      self._Tags.append(HTags.Tags)

    #--------------------------------------------------------------------------
  def _ProcessTags(self, _Line):
    '''
    Process the tags for a line.
    '''
    for Tags in self._Tags:
      LineLen = len(_Line)
      Offset = 0
      while Offset < LineLen:
        StrtTagOffset = _Line.find('@@@', Offset)
        if StrtTagOffset == -1: break
        if StrtTagOffset + 6 >= LineLen: break
        EndTagOffset = _Line.find('@@@', StrtTagOffset + 2)
        if EndTagOffset == -1: break
        if ' ' not in _Line[StrtTagOffset+3:EndTagOffset]:
          TagName = _Line[StrtTagOffset+3:EndTagOffset]
          EndTagOffset += 3
          if TagName in Tags.keys():
            TagInfo = Tags[TagName]
            if TagInfo.Type == TagTypes.SINGLEWORD:
              if isinstance(TagInfo.Value, str):
                _Line = _Line[0:StrtTagOffset] + TagInfo.Value + _Line[EndTagOffset:]
                Offset = StrtTagOffset + len(TagInfo.Value)
              else:
                _Line = _Line[0:StrtTagOffset] + ' '.join(TagInfo.Value) + _Line[EndTagOffset:]
                Offset = StrtTagOffset + len(' '.join(TagInfo.Value))
            elif TagInfo.Type == TagTypes.SENTENCE:
              if isinstance(TagInfo.Value, str):
                _Line = (' ' * StrtTagOffset) + TagInfo.Value + '\n'
              else:
                _Line = (' ' * StrtTagOffset) + ' '.join(TagInfo.Value) + '\n'
              return _Line
            elif TagInfo.Type == TagTypes.PARAGRAPH:
              if isinstance(TagInfo.Value, str):
                _Line = (' ' * StrtTagOffset) + TagInfo.Value + '\n'
              else:
                _Line = ''
                for xline in TagInfo.Value:
                  _Line += (' ' * StrtTagOffset) + xline + '\n'
              return _Line
            LineLen = len(_Line)
          else:
            Offset = EndTagOffset
        else:
          Offset = EndTagOffset + 3
      
    return _Line
  
    #--------------------------------------------------------------------------
  def _ProcessTopicTran(self):
    '''
    Process the TopicTran help file.
    '''
    self._TopicList = []

    TopicTranFileName = self._ExpandFileName('_TopicTran.help')
    if TopicTranFileName is None:
      raise HelpException('Unable to find _TopicTran.help file')

    try:
      with open(TopicTranFileName, 'r') as TopicTranFile:
        LineCnt = 0
        for line in TopicTranFile:
          LineCnt += 1
          line = line.strip()
          if line:
            TranData = line.split()

              # Process the last entry, to get the final topic file.
            FinalTopicFile = None
            FinalTopic = None
            if TranData[-1].startswith('f:'):
              if len(TranData) == 1:
                raise HelpException('Bad format of line at {0} in TopicTran help file {1}'.format(LineCnt,
                                                                                                  TopicTranFileName))

              FinalTopicFile = self._ExpandFileName(TranData[-1][2:])
              if FinalTopicFile is None:
                raise HelpException(f'Unable to find User Topic file {TranData[-1]}')
            else:
              FinalTopic = TranData[-1]
              if FinalTopic.startswith('t:'):  # TODO: Handle empty topic
                FinalTopic = FinalTopic[2:]
                self._TopicList.append(FinalTopic)
              FinalTopic = FinalTopic.strip()
              if not FinalTopic:
                raise HelpException('Bad format (missing topic) of line at {0} in TopicTran help file {1}'.format(LineCnt,
                                                                                                                  TopicTranFileName))
              FinalTopicFile = self._ExpandFileName(FinalTopic + '.help')
              if FinalTopicFile is None:
                raise HelpException('Unable to find Topic file {0} for Topic {1}'.format(FinalTopic + '.help',
                                                                                          TranData[-1]))
              if not FinalTopic in self._Topics.keys():
                self._Topics[FinalTopic] = FinalTopicFile

            TranData.pop(-1)

              # Process the rest of the trans data.
            while TranData:
              if TranData[-1] != '=>' and TranData[-1] != '->':
                raise HelpException('Bad format of line at {0} in TopicTran help file {1}'.format(LineCnt,
                                                                                                  TopicTranFileName))
              TranData.pop(-1)
              if not TranData:
                raise HelpException('Bad format of line at {0} in TopicTran help file {1}'.format(LineCnt,
                                                                                                  TopicTranFileName))
              FinalTopic = TranData[-1]
              if FinalTopic.startswith('t:'):
                FinalTopic = FinalTopic[2:]
                self._TopicList.append(FinalTopic)
              FinalTopic = FinalTopic.strip()
              if not FinalTopic:
                raise HelpException('Bad format (missing topic) of line at {0} in TopicTran help file {1}'.format(LineCnt,
                                                                                                                  TopicTranFileName))
              self._Topics[FinalTopic] = FinalTopicFile
              TranData.pop(-1)
    except HelpException as err:
      raise err from None
    except Exception as err:
      raise HelpException('Unable to open TopicTran help file {0} ({1})'.format(TopicTranFileName,
                                                                                str(err))) from FileNotFoundError

      # Lets sort the topiclist
    def SortFunc(e):
      return e.lower()

    self._TopicList.sort(reverse = False, key = SortFunc)

    #--------------------------------------------------------------------------
  def _ValidateTags(self, Tags):
    '''
    Validate the tags dictionary.  If invalid will raise an AttributeError.
    '''
    if not isinstance(Tags, dict):
      raise AttributeError('Tags must be None or a dictionary ({0})'.format(str(type(Tags))))

    for TagName, TagInfo in Tags.items():
      if not isinstance(TagName, str) or TagName == '' or TagName.find(' ') != -1:
        raise AttributeError('TagName can not be empty or contain spaces and must be a string')
      if str(type(TagInfo)) != "<class 'PythonLib.Help.Help.TagInfo'>":
        raise AttributeError('{0}: Tag items must be of type TagInfoDef ({1})'.format(TagName, 
                                                                                      str(type(TagInfo))))
      if not isinstance(TagInfo.Type, TagTypes):
        raise AttributeError('{0}: Type is not of TagTypes ({1})'.format(TagName, 
                                                                         str(type(TagInfo.Type))))
      if not isinstance(TagInfo.Value, (str, tuple, list)):
        raise AttributeError('{0}: Value is not string, tuple, or list ({1})'.format(TagName, 
                                                                                     str(type(TagInfo.Type))))
