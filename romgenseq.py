#!/usr/bin/env python
# 
# EBD generic question sequencing based on 
# ROM incidence matrix
#
# incidence codes
# 0 - no relation
# 1 - subject-verb relation
# 2 - verb-object relation
# 3 - particularizing/constraint relation
# 4 - sequencing relation
#

import functools;

@functools.total_ordering
class ObjectRel(object): 
  "store incoming links to object"
  def __len__(self): return len(self.rel)
  def __init__(self, oid=-1, rel=[]):
    self.oid = oid
    self.rel = rel
  def __repr__(self): return ('oid:%d<-' % self.oid) + str(self.rel)
  def __eq__(self, other): self.oid==other.oid and oid > 0
  def __lt__(self, other): 
    return len(self) > len(other)

# throw exception if matrix not square
def assertMatrixSqure(mat):
  expectedRowLen=len(mat)
  for row in mat:
    rowLen = len(row)
    if rowLen != expectedRowLen:
      raise Exception, (
        'Not a square matrix. '+
        'All rows must have length %d' % expectedRowLen)

# returns transpose of matrix
def transposed(mat): return zip(*mat)

# returns indexes of array elements having values > 0  
def nonZeroIndexes(numbers): 
  i=0
  nonZeroIndexes=[]
  for n in numbers:
    if n > 0:
      nonZeroIndexes+=[i]
    i+=1
  return nonZeroIndexes

def objectRel(rommat):
  """Transform square ROM association matrix to list of ObjectRel.

  index of ObjectRel in return list == oid-1"""

  assertMatrixSqure(rommat)
  oid=0
  rels=[]
  for inRel in transposed(rommat):
      oid+=1
      relOids = map(
        lambda i: i+1,  # oids start w/ 1, indexes w/ 0
        nonZeroIndexes(inRel))
      rels+=[ObjectRel(oid,relOids)]
  return rels;

def oidList(rels): return map(lambda r: r.oid, rels)

def d(o, msg=""):
  print(msg+" "+str(o))
  return o

def objectRelTraverse(rels):
  """Determine generic quesiton order for ROM diagram.

  args: 
    oids to visit, in order of importance
    rels list, ordered by oid
    returns oids to question for object"""

  # enable oid-based lookup w/o list indices
  relsDict=dict(    
    map(
      lambda rel: (rel.oid, rel), 
      rels))

  visited=set()
  
  def dfs(obj):
    traversal=[]
    if obj not in visited:
      visited.add(obj)
      for r in sorted(map(lambda r: relsDict[r], obj.rel)):
        traversal.extend(dfs(r))
      traversal.append(obj.oid)
    return traversal

  traversal=[]
  for o in sorted(rels):
    traversal.extend(dfs(o))
  return traversal
  
if __name__ == '__main__':
  import csv
  import sys
  import re
  outfileInfix=lambda s: "-traversal"+s.group(0)
  infile=sys.argv[1]
  # try to replace extension if available, or best attempt
  outfile=re.sub(r'\.?.{1,3}$', outfileInfix, infile)
  with open(infile, 'rb') as csvfile:
    reader=csv.reader(csvfile)
    rommat=[map(int, row) for row in reader]
    rels=objectRel(rommat)
    trav=objectRelTraverse(rels)
    print ",".join(map(str, trav))
