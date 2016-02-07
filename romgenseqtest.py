#!/usr/bin/env python
import unittest
import romgenseq

def rel(oid, rel=[]): return romgenseq.ObjectRel(oid, rel)
def oids(rels): return map(lambda r: r.oid, rels)

class RomGenSeqTest(unittest.TestCase):

  def test_ObjectRelEq(self):
    r1=romgenseq.ObjectRel(1)
    r2=romgenseq.ObjectRel(1)

    self.assertEqual(r1, r2)

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
    expectedOrder=[[2],[1],[3],[0]]
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

    expectedTrav=[[4],[5],[6],[7],[10],[11],[12],[13],[9],[8]]
    actualTrav=romgenseq.objectRelTraverse(rels)

    self.assertEqual(expectedTrav, actualTrav)

  def test_traversalShort(self):
    rels=[
      rel(5),
      rel(6),
      rel(7),
      rel(8, [5,6,7]),
    ]

    expectedTrav=[
        5,
        6,
        7,
        8,
        [5, 8], 
        [6, 8], 
        [7, 8]]
    actualTrav=romgenseq.objectRelTraverse(rels)

    self.assertEqual(expectedTrav, actualTrav)

  def test_traversalLinear(self):
    rels=[
      rel(4, [3]),
      rel(3, [2]), 
      rel(2, [1]), 
      rel(1, [] ) 
    ]

    expectedTrav=[
        [1],
        [2],
        [1, 2],
        [3], 
        [2, 3], 
        [1, 2, 3], 
        [4], 
        [3, 4], 
        [2, 3, 4], 
        [1, 2, 3, 4]]

    actualTrav=romgenseq.objectRelTraverse(rels)

    print "TEST RESULTS"
    for t in actualTrav: print t
    self.assertEqual(expectedTrav, actualTrav)

  def test_traversalLinearReverse(self):
    rels=[
      rel(1, [] ), 
      rel(2, [1]), 
      rel(3, [2]), 
      rel(4, [3])
    ]

    expectedTrav=[
        [1],
        [2],
        [1, 2],
        [3], 
        [2, 3], 
        [1, 2, 3], 
        [4], 
        [3, 4], 
        [2, 3, 4], 
        [1, 2, 3, 4]]

    actualTrav=romgenseq.objectRelTraverse(rels)

    print "TEST RESULTS"
    for t in actualTrav: print t
    self.assertEqual(expectedTrav, actualTrav)

  def test_traversal(self):
    """1-3 and 5-9 form disconnected subgraphs"""
    rels=[
      rel(1, [3]),
      rel(2),
      rel(3, [1,2]),
      rel(5),
      rel(6),
      rel(7),
      rel(8, [5,6,7]),
    ]

    expectedTrav=[[5],[6],[7],[8],[1],[2],[3]]
    actualTrav=romgenseq.objectRelTraverse(rels)

    self.assertEqual(expectedTrav, actualTrav)

  def test_labelingOfOids(self):
    import rommodel
    oids=[2,3,1]
    words=[
        rommodel.ROMObject('a', 1),
        rommodel.ROMObject('b', 2),
        rommodel.ROMObject('c', 3)]

    wordsInOrder=romgenseq.orderRomObjectsByOid(words,oids)

    expectedOrder=[
        words[1], 
        words[2], 
        words[0]]

    self.assertEqual(expectedOrder, wordsInOrder)


if __name__ == '__main__':
  unittest.main()
