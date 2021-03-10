import unittest

from Libs.Base.CreationInfo import (CCreationInfo , InstanceCreationError)  # pylint: disable=unused-import


class CMyCreationInfo(unittest.TestCase):

  def test_TestSingle(self):

    class CSingleClass(CCreationInfo):

      def __init__(self):
        CCreationInfo.__init__(self)

      @property
      def RClassName(self):
        return self.ClassName

      @property
      def RCreationFile(self):
        return self.CreationFile

      @property
      def RCreationModule(self):
        return self.CreationModule

      @property
      def RInstanceName(self):
        return self.InstanceName

    SingleClass = CSingleClass()
    SingleClass1 = CSingleClass()

    self.assertEqual(SingleClass.RClassName, "CSingleClass")
    self.assertEqual(SingleClass.RCreationFile, __file__)
    self.assertEqual(SingleClass.RCreationModule, "Libs.Base.tests.test_CreationInfo")
    self.assertEqual(SingleClass.RInstanceName, "SingleClass")

    self.assertEqual(SingleClass1.RClassName, "CSingleClass")
    self.assertEqual(SingleClass1.RCreationFile, __file__)
    self.assertEqual(SingleClass1.RCreationModule, "Libs.Base.tests.test_CreationInfo")
    self.assertEqual(SingleClass1.RInstanceName, "SingleClass1")

  def test_MutliLevel(self):

    class CMClass1(CCreationInfo):

      def __init__(self):
        CCreationInfo.__init__(self)

      @property
      def RClassName(self):
        return self.ClassName

      @property
      def RCreationFile(self):
        return self.CreationFile

      @property
      def RCreationModule(self):
        return self.CreationModule

      @property
      def RInstanceName(self):
        return self.InstanceName

    class CMClass2(CMClass1):

      def __init__(self):
        CMClass1.__init__(self)

      @property
      def RClassName(self):
        return self.ClassName

      @property
      def RCreationFile(self):
        return self.CreationFile

      @property
      def RCreationModule(self):
        return self.CreationModule

      @property
      def RInstanceName(self):
        return self.InstanceName

    MClass1 = CMClass1()
    MClass2 = CMClass2()

    self.assertEqual(MClass1.RClassName, "CMClass1")
    self.assertEqual(MClass1.RCreationFile, __file__)
    self.assertEqual(MClass1.RCreationModule, "Libs.Base.tests.test_CreationInfo")
    self.assertEqual(MClass1.RInstanceName, "MClass1")

    self.assertEqual(MClass2.RClassName, "CMClass2")
    self.assertEqual(MClass2.RCreationFile, __file__)
    self.assertEqual(MClass2.RCreationModule, "Libs.Base.tests.test_CreationInfo")
    self.assertEqual(MClass2.RInstanceName, "MClass2")

  def test_Creation(self):
    MClass1 = CCreationInfo()
    self.assertEqual(MClass1.ClassName, "CCreationInfo")
    self.assertEqual(MClass1.CreationFile, __file__)
    self.assertEqual(MClass1.CreationModule, "Libs.Base.tests.test_CreationInfo")
    self.assertEqual(MClass1.InstanceName, "MClass1")


if __name__ == "__main__":
  unittest.main()  # pragma: no cover
