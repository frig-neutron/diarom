#!/usr/bin/env python
import unittest
import romgenseq

def rel(oid, rel=[]): return romgenseq.ObjectRel(oid, rel)
def oids(rels): return map(lambda r: r.oid, rels)

class RomGenSeqTest(unittest.TestCase):
  def test_rommat2rels(self): 
    rommat=[
      [0, 2, 0],
      [0, 0, 3],
      [1, 0, 3],
    ]

    rels=romgenseq.objectRel(rommat)

    self.assertEqual(len(rels), 3)
    self.assertEqual(rels[0].oid, 1)
    self.assertEqual(rels[0].rel, [3])
    self.assertEqual(rels[1].oid, 2)
    self.assertEqual(rels[1].rel, [1])
    self.assertEqual(rels[2].oid, 3)
    self.assertEqual(rels[2].rel, [2,3])

  def test_traverseRelOrder(self):
    rels=[
      rel(0,[1,2,3]),
      rel(1),
      rel(2, [0]), 
      rel(3),
    ]
    expectedOrder=[2,1,3,0]
    actualOrder=romgenseq.objectRelTraverse(rels)
    self.assertEqual(expectedOrder, actualOrder)

  def test_traversalConnected(self):
    rels=[
      rel(4, [5]), 
      rel(5, [4,8]),
      rel(6),
      rel(7, [6]),
      rel(8, [5,6,7,9]),
      rel(9, [13]),
      rel(10),
      rel(11),
      rel(12, [10,11]),
      rel(13, [9,12])
    ]

    expectedTrav=[4,5,6,7,10,11,12,13,9,8]
    actualTrav=romgenseq.objectRelTraverse(rels)

    self.assertEqual(expectedTrav, actualTrav)

  def test_traversal(self):
    rels=[
      rel(1, [3]),
      rel(2),
      rel(3, [1,2]),
      rel(5),
      rel(6),
      rel(7),
      rel(8, [5,6,7]),
    ]

    expectedTrav=[5,6,7,8,1,2,3]
    actualTrav=romgenseq.objectRelTraverse(rels)

    self.assertEqual(expectedTrav, actualTrav)



if __name__ == '__main__':
  unittest.main()
