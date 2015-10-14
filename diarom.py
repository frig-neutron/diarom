#!/usr/bin/env python

import rommodel
import rominput

REL_CONSTRAINT=1
REL_SUB2VERB=2
REL_VERB2OBJ=3
REL_OTHER=4

def name_of(obj):
  """Find the text from the label of boxy shape thing."""
  obj_type=obj.type.name
  if obj_type == 'ER - Entity':
    return obj.properties['name'].value
  if obj_type == 'Flowchart - Box':
    return obj.properties['text'].value.text

def mkRomRelation(diaLine):

  ARROW_TYPE_NONE=0
  ARROW_TYPE_PLAIN=1
  ARROW_TYPE_BALL_FILLED_BLACK=8
  ARROW_TYPE_BALL_FILLED_WHITE=9
  ARROW_TYPE_STARFLEET_FILLED=22
  ARROW_TYPE_STARFLEET_HOLLOW=23
  ARROW_TYPE_TRIANGLE_FILLED_BLACK=3
  ARROW_TYPE_TRIANGLE_FILLED_WHITE=2
  ARROW_TYPE_TRIANGLE_HOLLOW=12
  ARROW_TYPE_RECT_STRIKE_FILLED_BLACK=16
  ARROW_TYPE_RECT_STRIKE_FILLED_WHITE=17

  def arrowhead(which): return diaLine.properties[which+'_arrow'].value.type

  arrow_start=arrowhead('start')
  arrow_end=arrowhead('end')
  line_style,_=diaLine.properties['line_style'].value

  if line_style > 0:
    rel_type = REL_OTHER
  elif arrow_start == ARROW_TYPE_BALL_FILLED_BLACK:
    rel_type = REL_CONSTRAINT
  elif arrow_start == ARROW_TYPE_NONE:
    rel_type = REL_VERB2OBJ
  elif arrow_start == ARROW_TYPE_RECT_STRIKE_FILLED_BLACK:
    rel_type = REL_SUB2VERB
  else:
    raise Exception(
      "Don't know rel type. Line style="+str(
        line_style)+" start_arrow="+str(
        arrow_start)+" end_arrow="+str(arrow_end))

  def connected_obj(hIdx): 
    """Return ROMObject instance representing connection endpoint"""
    connected_to=diaLine.handles[hIdx].connected_to
    if connected_to is None:
      dia.active_display().diagram.select(diaLine)
      dia.active_display().flush()
      print(diaLine)
    else:
      name = name_of( connected_to.object )
      return rommodel.ROMObject( name )

  pointer_obj = connected_obj(0)
  pointee_obj = connected_obj(1)  # PolyLines + others use different indexing

  return ROMRelation(pointer_obj, pointee_obj, rel_type) 

class ROMRelation(object): 
  
  def __init__(self, pointer_obj, pointee_obj, rel_type): 
    self.pointer_obj = pointer_obj
    self.pointee_obj = pointee_obj
    self.rel_type = rel_type
    self.symmetric = rel_type == REL_SUB2VERB or rel_type == REL_VERB2OBJ

# TODO: make this function a method of some ROMObjects collection class.
#       Then nElements will not be required since the collection can count
#       the number of distinct OIDs it has.
def dictMatrixToListMatrix(dictMatrix, nElements):
  """Convert dict-based matrix representation to list-based square matrix.

    Dict-based matrix is a hash-o-hashes. Logically it's From -> To -> RelType.
    Dict keys may be numerical oids or ROMObject instances.
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

def rom_object_draw(data, words):
  import dia
  boxType=dia.get_object_type("Flowchart - Box")
  layer=data.active_layer

  for word in reversed(words):
    box, h1, h2=boxType.create(0,0)
    box.properties['text'] = str(word)
    layer.add_object(box)

def import_romtext(inFile, diagramData):
  import dia
  parser = rominput.ROMInputParser()

  f = open(inFile)
  for line in f:
    words = parser.parse_words(line)
    rom_object_draw(diagramData, words)

  dia.active_display().add_update_all()
  dia.active_display().flush()

class MaxRegister:
  def __init__(self):
    self.max=0

  def set(self, x):
    if self.max < x: 
      self.max=x

class ROMRenderer: 

  def begin_render (self, data, filename):
    """DiaRenderer interface method"""

    def is_line(o): 
      return o.type.name == 'Standard - Line' or o.type.name == 'Standard - PolyLine'

    objects=data.active_layer.objects
    relations = [mkRomRelation(obj) for obj in objects if is_line(obj)]

    incidenceHash={} # hash-o-hashes: pointer obj -> { pointee obj -> rel type }
    maxOid=MaxRegister()

    def relation(rel_from, rel_to, rel_type):
      maxOid.set(rel_from.oid)
      maxOid.set(rel_to.oid)

      if rel_from not in incidenceHash: 
        incidenceHash[rel_from] = {}

      pointees=incidenceHash[rel_from]
      pointees[rel_to]=rel_type

    for rel in relations: 
      relation( rel.pointer_obj, rel.pointee_obj, rel.rel_type)
      if rel.symmetric: 
        relation (rel.pointee_obj, rel.pointer_obj, rel.rel_type)
      
    f=open(filename, 'w')
    incidenceMatrix=dictMatrixToListMatrix(incidenceHash, maxOid.max)
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

  inFile=sys.argv[1]
  parser = rominput.ROMInputParser()
  f=open(inFile)
  for line in f:
    words=parser.parse_words(line)
    print words
else:
  try:
    import dia
    dia.register_import ("ROM Text2Obj", "txt", import_romtext)
    dia.register_export ("ROM Incidence Matrix", "csv", ROMRenderer())
  except ImportError, e: 
    pass

