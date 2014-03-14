#!/usr/bin/env python
import unittest
import diarom

def rel(oid, rel=[]): return romgenseq.ObjectRel(oid, rel)
def oids(rels): return map(lambda r: r.oid, rels)

class DiaRomTest(unittest.TestCase):

  def test_romObjectParse(self):
    text='voorwerp [42]'
    obj=diarom.ROMObject(text)

    self.assertEqual(42, obj.oid)
    self.assertEqual('voorwerp', obj.text)

  def test_romObjectRepr(self):
    obj=diarom.ROMObject('voorwerp', 42)
    repr=str(obj)
    self.assertEqual('voorwerp [42]', repr)

  def test_romObjectHashBasedOnOid(self):
    obj=diarom.ROMObject('voorwerp', 42)
    hash=obj.__hash__()
    self.assertEqual(42, hash)

  def test_romObjectsShouldBeEqualIfOidsEqual(self):
    obj1=diarom.ROMObject('voorwerp1', 42)
    obj2=diarom.ROMObject('voorwerp2', 42)
    self.assertEqual(obj1, obj2)
    
  def test_romObjectsShouldBeNotEqualIfOidsNotEqual(self):
    obj1=diarom.ROMObject('voorwerp', 42)
    obj2=diarom.ROMObject('voorwerp', 43)
    self.assertNotEqual(obj1, obj2)
    

if __name__ == '__main__':
  unittest.main()

