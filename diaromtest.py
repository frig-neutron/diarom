#!/usr/bin/env python
import unittest
import diarom

def rel(oid, rel=[]): return romgenseq.ObjectRel(oid, rel)
def oids(rels): return map(lambda r: r.oid, rels)

class DiaRomTest(unittest.TestCase):
  def test_convertEmptyDictMatrixToSquareMatrix(self):
    nElements=3
    dictMatrix={}
    listMatrix=[[0] * nElements] * nElements
    actual=diarom.dictMatrixToListMatrix(dictMatrix, nElements)
    self.assertEqual(actual, listMatrix)

  def test_convert2x2DictMatrixToListMatrix(self):
    nElements=2
    dictMatrix={
      2: {1: 1},
    }
    listMatrix=[
      [0, 0], 
      [1, 0],
    ]
    actual=diarom.dictMatrixToListMatrix(dictMatrix, nElements)
    self.assertEqual(actual, listMatrix)

  def testConvert3x3DictMatrixToListMatrix(self):
    nElements=3
    dictMatrix={1:{}, 2:{}, 3:{}}

    dictMatrix[1].update( {1: 1} )
    dictMatrix[1].update( {2: 2} )
    dictMatrix[1].update( {3: 3} )
    dictMatrix[2].update( {1: 4} ) 
    dictMatrix[2].update( {2: 5} )
    dictMatrix[2].update( {3: 6} )
    dictMatrix[3].update( {1: 7} )
    dictMatrix[3].update( {2: 8} )
    dictMatrix[3].update( {3: 9} )

    listMatrix=[
      [1, 2, 3], 
      [4, 5, 6],
      [7, 8, 9],
    ]
    actual=diarom.dictMatrixToListMatrix(dictMatrix, nElements)
    self.assertEqual(actual, listMatrix)
    

if __name__ == '__main__':
  unittest.main()

