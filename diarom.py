#!/usr/bin/env python

class ROMObject(object): 
  def __init__(self, text, oid=None):

    openIndex=text.find('[')
    closeIndex=text.find(']')

    def parseOid(): return int(text[openIndex+1:closeIndex])
    def stripOid(): return text[0:openIndex].strip()
    
    if not oid: 
      oid = parseOid()
      text = stripOid()

    self.oid = oid
    self.text = text.strip()

  def __repr__(self): return self.text+' ['+str(self.oid)+']'
  def __hash__(self): return self.oid
  def __int__(self): return self.oid
  def __eq__(self, other): return self.oid == other.oid


class ROMParseResult:
  words=[]
  indexedInput=''

class ROMObjectFactory(object): 
  def __init__(self):
    self.wordCount=0

  def parse_words(self, words):
    class ParseContext:
      def __init__(dasInnerIch):
        dasInnerIch.words=[]
        dasInnerIch.wordsIndexed=''
        dasInnerIch.inWord=False
        dasInnerIch.word=''

    ctx=ParseContext()

    def next_word():
      self.wordCount+=1
      sufx='['+str(self.wordCount)+']'
      ctx.word+=sufx
      ctx.wordsIndexed+=sufx
      ctx.words+=[ctx.word]

    for c in words:
      if c.isalnum():
        ctx.word+=c
        ctx.wordsIndexed+=c
        ctx.inWord=True       
      else:
        if ctx.inWord:
          # end of word
          next_word()
        ctx.inWord=False
        ctx.wordsIndexed+=c
        ctx.word=''
    if ctx.inWord:
      next_word()

    ret=ROMParseResult()
    ret.words = ctx.words
    ret.indexedInput = ctx.wordsIndexed
    return ret

  def rom_object_gen(self, data, string):
    import dia
    boxType=dia.get_object_type("Flowchart - Box")
    layer=data.active_layer

    parsed=self.parse_words(string)
    for word in reversed(parsed.words):
      box, h1, h2=boxType.create(0,0)
      box.properties['text'] = word
      layer.add_object(box)

# TODO: make this function a method of some ROMObjects collection class.
#       Then nElements will not be required since the collection can count
#       the number of distinct OIDs it has.
def dictMatrixToListMatrix(dictMatrix, nElements):
  """Convert dict-based matrix representation to list-based square matrix.

    Dict-based matrix is a hash-o-hashes. Logically it's From -> To -> RelType.
    Dict keys may be interchangeably numericals or ROMObject instances.
    nElements is required because the hash may be sparse, resulting in fewer 
    rows than objects in diagram. Thus, must count externally.
    """
  listMat=[[0]*nElements]*nElements
  for obj_from in dictMatrix:
    idx_from=int(obj_from)-1
    listMat[idx_from]=[0]*nElements
    for obj_to in dictMatrix[obj_from]:
      idx_to=int(obj_to)-1
      listMat[idx_from][idx_to]=dictMatrix[obj_from][obj_to]

  return listMat

def import_romtext(inFile, diagramData):
  import dia
  fact=ROMObjectFactory()
  f = open(inFile)
  text=''
  for line in f:
    text+=line
  fact.rom_object_gen(diagramData, text)

  dia.active_display().add_update_all()
  dia.active_display().flush()

REL_CONSTRAINT=1
REL_SUB2VERB=2
REL_VERB2OBJ=3
REL_OTHER=4

class ROMRenderer: 

  def rel_type(self, diaRel):
    """Identify what type of ROM relation the dia line represents."""
    return REL_CONSTRAINT   #TODO: examine the arrow

  # TODO: look into enum type capabililty. If enum supports methods, replace rel types 
  #       with enums and make this enum instance method
  def is_symmetric_rel(self, rel):
    """Identify whether the relation is symmetric or not.
      Only verb relations are symmetric.  """
    return False #TODO: if rel is Line type, find rel_type, if not return true if 2 or 3 else false

  def name_of(self, obj):
    """Find the text from the label of boxy shape thing."""
    obj_type=obj.type.name
    if obj_type == 'ER - Entity':
      return obj.properties['name'].value
    if obj_type == 'Flowchart - Box':
      return obj.properties['text'].value.text

  def connected_obj(self, rel, hIdx): 
    name = self.name_of( rel.handles[hIdx].connected_to.object )
    return ROMObject( name )

  def pointer_obj(self, rel): return self.connected_obj(rel, 0)

  def pointee_obj(self, rel): return self.connected_obj(rel, 1)

  def begin_render (self, data, filename):
    """DiaRenderer interface method"""
    lines = filter(
      lambda o: o.type.name == 'Standard - Line', 
      data.active_layer.objects)

    incidenceHash={} # hash-o-hashes: pointer obj -> { pointee obj -> reltype }
    uniqueObjects=set()
    def relation(rel_from, rel_to, rel_type):
      uniqueObjects.add(rel_from)
      uniqueObjects.add(rel_to)

      if rel_from not in incidenceHash: 
        incidenceHash[rel_from] = {}

      pointees=incidenceHash[rel_from]
      pointees[rel_to]=rel_type

    for rel in lines: 
      rel_type = self.rel_type(rel)
      sym = self.is_symmetric_rel(rel)
      relation( self.pointer_obj(rel), self.pointee_obj(rel), rel_type)
      if sym: # reverse relationship
        relation ( pointee_obj(rel), pointer_obj(rel), rel_type)
      
    f=open(filename, 'w')
    incidenceMatrix=dictMatrixToListMatrix(incidenceHash, len(uniqueObjects))
    for row in incidenceMatrix:
      rowstr=','.join(str(x) for x in row)
      f.write(rowstr)
      f.write('\n')
    f.close

  def end_render(self):
    """DiaRender interface method"""
    pass

if __name__ == '__main__':
  import sys
  fact=ROMObjectFactory()

  inFile=sys.argv[1]
  f=open(inFile)
  for line in f:
    words=fact.parse_words(line)
    print words.words
else:
  try:
    import dia
    dia.register_import ("ROM Text2Obj", "txt", import_romtext)
    dia.register_export ("ROM Incidence Matrix", "csv", ROMRenderer())
  except ImportError, e: 
    pass

