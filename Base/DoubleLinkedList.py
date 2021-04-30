'''
Created:   Apr 30, 2021
Author:    Donald W. Long (Donald.W.Long@gmail.com)
-----------------------------------------------------------------------------
CopyRight:

    Copyright (C) 2020-2021  Donald W. Long (Donald.W.Long@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
Description:

  Implements a doubly linked list.
-----------------------------------------------------------------------------
Update History:
  Author: Donald W. Long (Donald.W.Long@gmail.com)
  Date:   Apr 30, 2021
    Released
-----------------------------------------------------------------------------
'''

from enum import (IntEnum, unique, auto)


  #======================================================
@unique
class DLinkType(IntEnum):
  '''
  Defines the types of doubly linked list your can have
    FIFO
      First in First out
    LIFO
      Last in First out
  '''
  FIFO = auto()
  LIFO = auto()


  #======================================================
class CNode:
  '''
  Is the Node definition for each node in the double linked
  List. Be careful with writing to the variables in this.
  Prev and Next are managed by CDoubleLinkedList.  You can
  change the user data all your wish.  It is not used by
  CDoubleLinkedList, its your data.

    CNode(UserData)
      UserData
        Is the data you wish to store in the node.

    Prev
      Is the previous Node.  Until its placed in the double
      linked list it is None.
    Next
      Is the next Node.  Until its placed in the double
      linked list it is None.
    UserData
      Is the 'Data' argument that was passed in to CNode.
  '''

  def __init__(self, UserData):
    self.Prev = None
    self.Next = None
    self.UserData = UserData


  #======================================================
class CDoubleLinkedList(object):
  '''
  Is the double linked list.  When you create this you
  select the type you wish, FIFO or LIFO.  See the enum
  DLinkType.  This class supports iteration thru the
  list just like a python list.

    DList = CDoubleLinkedList(Type)
      Type
        Is DLinkType.FIFO or DLinkType.LIFO

  Exceptions:
    AttributeError
      If type is not of DLinkType
  '''

  def __init__(self, Type):
    object.__init__(self)

    if not isinstance(Type, DLinkType):
      raise AttributeError(f'Type must be of DLinkType: {type(Type)}')
    self._Type = Type
    self._Cnt = 0
    self._CurNode = None
    self._FirstNode = None

    #------------------------------------------------------    #------------------------------------------------------
  @property
  def Count(self):
    '''
    Property: is the number of items in the list
    '''
    return self._Cnt

    #------------------------------------------------------
  def IsNode(self, Node):
    '''
    Checks to see if the passed in Node is part of this
    doubly linked list.

      RNode = IsNode(Node)
        RNode
          If part of the doubly linked list will be the
          same node that you passed in, else None
        Node
          Is the node to check
    '''
    FoundNode = None

    if self._Cnt and Node:
      SavedCurNode = self._CurNode
      self._CurNode = None
      for FoundNode in self:
        if FoundNode == Node:
          break
      self._CurNode = SavedCurNode

    return FoundNode

    #------------------------------------------------------
  def Next(self):
    '''
    It returns the next node in the list.  If its the first
    time its been called it returns the first item.  Every
    call after that returns the next until no more items in
    the list.

      Node = Next()
        Node
          Is the node from the list. When no more nodes will
          return None
    '''
    Node = None

    if self._Cnt:
      if not self._CurNode:
        Node = self._CurNode = self._FirstNode
      else:
        if self._CurNode.Next != self._FirstNode:
          Node = self._CurNode.Next
          self._CurNode = Node
        else:
          self._CurNode = None

    return Node

    #------------------------------------------------------
  def Pop(self):
    '''
    Pops the first item off the list. If empty return None.

      Node = Pop()
        Node
          Is the node else None if empty.  The returned
          node is no longer part of this doubly linked list.
    '''
    return self.PopTop()

    #------------------------------------------------------
  def PopTop(self):
    '''
    Pops the first item off the list. If empty return None.

      Node = PopTop()
        Node
          Is the node else None if empty.  The returned
          node is no longer part of this doubly linked list.
    '''
    Node = self._FirstNode

    if self._Cnt:
      self._Cnt -= 1
      if not self._Cnt:
        self._FirstNode = None
        self._CurNode = None
      else:
        self._FirstNode = Node.Next
        Node.Prev.Next = Node.Next
        Node.Next.Prev = Node.Prev
        if self._CurNode == Node:
          self._CurNode = None

      Node.Prev = Node.Next = None

    return Node

    #------------------------------------------------------
  def PopBottom(self):
    '''
    Pops the last item off the list. If empty return None.

      Node = PopBottom()
        Node
          Is the node else None if empty.  The returned
          node is no longer part of this doubly linked list.
    '''
    Node = None

    if self._Cnt:
      Node = self._FirstNode.Prev
      self._Cnt -= 1
      if not self._Cnt:
        self._Cnt = 0
        self._FirstNode = None
        self._CurNode = None
      else:
        Node.Prev.Next = Node.Next
        Node.Next.Prev = Node.Prev
        if self._CurNode == Node:
          self._CurNode = None

      Node.Prev = Node.Next = None

    return Node

    #------------------------------------------------------
  def PopNode(self, Node):
    '''
    Pops the node item off the list. If empty return None or
    if the Node is not part of this doubly linked list.

      RNode = PopNode(Node)
        RNode
          Is the node that you requested to be popped off.
          If it is not part of the doubly linked list will
          be None
        Node
          Is the node else None if empty.  The returned
          node is no longer part of this doubly linked list.
    '''
    FoundNode = self.IsNode(Node)
    if FoundNode:
      if Node == self._FirstNode:
        self.PopTop()
      else:
        SavedNode = self._FirstNode
        self._FirstNode = Node
        self.PopTop()
        self._FirstNode = SavedNode
        if self._CurNode == Node:
          self._CurNode = None

      Node.Prev = Node.Next = None

    return FoundNode

    #------------------------------------------------------
  def Push(self, UserData):
    '''
    Push's a node on the list.  It will create the node for
    you and assign the passed in user data to that node.
    How it gets pushed depends on the type of doubly linked
    list.

      Node = Push(UserData)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        UserData
          Is the data to assign to the node.
    '''
    if self._Type == DLinkType.FIFO:
      return self.PushBottomNode(CNode(UserData))

    return self.PushTopNode(CNode(UserData))

    #------------------------------------------------------
  def PushBeforeNode(self, BeforeNode, Node):
    '''
    Push's a node before the passed in node.

      RNode = PushBeforeNode(BeforeNode, Node)
        RNode
          Is your passed in Node, unless BeforeNode is not
          part of this doubly linked list, it will be None.
        BeforeNode
          Is the node to place the new node before.
        Node
          Is the data to assign to the node.
    '''
    if self.IsNode(BeforeNode):
      SavedFirstNode = self._FirstNode
      SavedCurNode = self._CurNode
      self._FirstNode = BeforeNode
      SavedType = self._Type
      self._Type = DLinkType.FIFO

      Node = self.PushTopNode(Node)

      if SavedFirstNode:
        self._FirstNode = SavedFirstNode
        self._CurNode = SavedCurNode
        self._Type = SavedType
    else: return None

    return Node

    #------------------------------------------------------
  def PushBeforeUserData(self, BeforeNode, UserData):
    '''
    Push's a node before the passed in node.  It creates
    the new node and places it before the based in node.

      Node = PushBeforeNode(BeforeNode, UserData)
        Node
          Is the new node that was created and placed in the
          doubly linked list.  If the BeforeNode is not part
          of this doubly linked list then None is returned.
        BeforeNode
          Is the node to place the new node before.
        UserData
          Is the data to assign to the node.
    '''
    return self.PushBeforeNode(BeforeNode, CNode(UserData))

    #------------------------------------------------------
  def PushBottom(self, UserData):
    '''
    Push's a node on the bottom of the list.  It will create
    the node for you and assign the passed in user data to that node.

      Node = PushBottom(UserData)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        UserData
          Is the data to assign to the node.
    '''
    return self.PushBottomNode(CNode(UserData))

    #------------------------------------------------------
  def PushBottomNode(self, NewNode):
    '''
    Push's a node on the bottom of the list.

      Node = PushBottom(NewNode)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        NewNode
          Is the node to push to the bottom.
    '''
    if self._Cnt == 0:
      NewNode.Prev = NewNode
      NewNode.Next = NewNode
      self._FirstNode = NewNode
    else:
      NewNode.Prev = self._FirstNode.Prev
      NewNode.Next = self._FirstNode
      NewNode.Prev.Next = NewNode
      self._FirstNode.Prev = NewNode

    self._Cnt += 1
    return NewNode

    #------------------------------------------------------
  def PushNode(self, NewNode):
    '''
    Push's a node on the list.  How it gets pushed depends
    on the type of doubly linked list.

      Node = Push(NewNode)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        NewNode
          Is the node to push.
    '''
    if self._Type == DLinkType.FIFO:
      return self.PushBottomNode(NewNode)

    return self.PushTopNode(NewNode)

    #------------------------------------------------------
  def PushTop(self, UserData):
    '''
    Push's a node on the top of the list.  It will create
    the node for you and assign the passed in user data to that node.

      Node = PushBottom(UserData)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        UserData
          Is the data to assign to the node.
    '''
    return self._PushTop(CNode(UserData))

    #------------------------------------------------------
  def PushTopNode(self, NewNode):
    '''
    Push's a node on the top of the list.

      Node = PushBottom(NewNode)
        Node
          Is the new node that was created and placed in the
          doubly linked list.
        NewNode
          Is the node to push to the top of the doubly linked
          list.
    '''
    if self._Cnt == 0:
      NewNode.Prev = NewNode
      NewNode.Next = NewNode
      self._FirstNode = NewNode
    else:
      NewNode.Prev = self._FirstNode.Prev
      NewNode.Next = self._FirstNode
      self._FirstNode.Prev = NewNode
      NewNode.Prev.Next = NewNode
      self._FirstNode = NewNode

    self._Cnt += 1
    return NewNode

    #------------------------------------------------------
  @property
  def Type(self):
    return self._Type

    #------------------------------------------------------
  def __iter__(self):
    self._CurNode = None
    return self

    #------------------------------------------------------
  def __next__(self):
    Node = self.Next()
    if not Node:
      raise StopIteration
    return Node
