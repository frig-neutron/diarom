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
  def __eq__(self, other): return self.oid==other.oid and self.oid > 0
  def __lt__(self, other): 
    return len(self) > len(other)

# throw exception if matrix not square
def assertMatrixSquare(mat):
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


def isPrefix(prefix, list):
  """Return true if prefix is a sublist of list, starting at element 0"""
  if len(list) < len(prefix): return False
  for pair in zip(prefix, list):
    if not pair[0] == pair[1]: 
      return False
  return True

def isSublist(sub, list): 
  "Return true if list contains sub as sublist"
  if [] == sub == list: return True
  for i in range(0,len(list)):
    if isPrefix(sub, list[i:]): return True
  return False

def isNonIdentitySublist(sub, list): 
  return isSublist(sub, list) and not sub is list

def isSublistOfSomeList(subCandidate, lists): 
  extensions = filter(
    lambda l: isNonIdentitySublist(subCandidate, l), 
    lists)
  return len(extensions) > 0

def uniqueSublists(listOfLists):
  """Retain lists that are not subes of other lists.
  
  Return list of lists which are not subes of each other.
  """
  return [ l for l in listOfLists if not isSublistOfSomeList(l, listOfLists) ]

def objectRel(rommat):
  """Transform square ROM association matrix to list of ObjectRel.

  index of ObjectRel in return list == oid-1"""

  assertMatrixSquare(rommat)
  oid=0
  rels=[]
  # Transposing because orig matrix stores link types 
  # from colIdx to rowIdx
  for inRel in transposed(rommat):
      oid+=1
      relOids = map(
        lambda i: i+1,  # oids start w/ 1, indexes w/ 0
        nonZeroIndexes(inRel))
      rels+=[ObjectRel(oid,relOids)]
  return rels;

def oidList(rels): return map(lambda r: r.oid, rels)

def objectRelTraverse(rels):
  """Determine generic quesiton order for ROM diagram.

  args: 
    rels list, ordered by oid
    returns oids to question for object"""

  # enable oid-based lookup w/o list indices
  relsDict=dict(    
    map(
      lambda rel: (rel.oid, rel), 
      rels))

  visited={}
  
  class C:
      def __init__(self): self.c = 0
      def inc(self): self.c = self.c+1
      def dec(self): self.c = self.c - 1
      def val(self): return self.c
      def p(self, msg): print (("  "*self.val())+str(msg))

  log = C()


  def dfs(obj):
    """Traverse object constraint subgraph and enumerate phrases.
    
      returns list of oid-phrases resulting from traversal, starting with the 
      oid of the obj param, if not yet visited, and ending with the longest phrase 
      in this subgraph.
    """
    log.inc()
    log.p("DFS "+str(obj))
    traversal=[]
    if obj in visited:
        traversal=visited[obj]
    else:   
      visited[obj] = [] # combat recusive loop
      constraints=map(lambda r: relsDict[r], obj.rel)
      allExtendedPhrases=[]
      for r in sorted(constraints):
        phrases=dfs(r)
        traversal.extend(phrases) # carry forward

        def isDirectConstraint(ph): 
            isConstraint = ph[-1] in obj.rel
            log.p('does '+str(ph)+' constrain '+str(obj)+'? '+str(isConstraint))
            return isConstraint

        extendedPhrases=[ ph + [obj.oid] for ph in phrases if isDirectConstraint(ph) ]
        allExtendedPhrases.append(extendedPhrases)

      traversal.append([obj.oid])
      for phrase in allExtendedPhrases: traversal.extend(phrase)
      visited[obj] = traversal

    log.p("result="+str(traversal))
    log.dec()
    return traversal

  paths=[]
  log.p(sorted(rels))
  for o in sorted(rels):
    log.p( "\nTOP LEVEL: "+str(o))
    t=dfs(o)
    paths.append(t)

  paths=uniqueSublists(paths)
  traversal=[]
  log.p( "PATHS")
  for path in paths: 
    log.p(path)
    traversal.extend(path)
  log.p("\nR"+str(traversal))
  return traversal

def orderRomObjectsByOid(romObjects,oidOrder):
  """Put ROM objects into order specified by OID list.
  
  args: 
    oids showing desired order of words
    romobjects list, to perform lookups in

  returns: 
    words from romobjects list, in the order they appear in oidOrder
  """
  romoids=map(int, romObjects)
  indexes=map(romoids.index, oidOrder)
  ordered=map(romObjects.__getitem__, indexes)
  return ordered

def printOids(oids): 
  print ",".join(map(str, oids))

def printWords(oidOrder, originalTextFile): 
  import rominput
  romObjects=rominput.read_file(originalTextFile)
  for phraseOids in oidOrder: 
    ordered=orderRomObjectsByOid(romObjects, phraseOids)
    for o in ordered: 
      print "%4d %s" % (o.oid, o.text)
  
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
    if len(sys.argv) == 2: 
      printOids(trav)
    elif len(sys.argv) == 3: 
      printWords(trav, sys.argv[2])
    else: 
      print "invocation error"
