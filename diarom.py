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


if __name__ == '__main__':
  import sys
  fact=ROMObjectFactory()

  inFile=sys.argv[1]
  f=open(inFile)
  for line in f:
    words=fact.parse_words(line)
    print words.words
else:
  import dia
  dia.register_import ("ROM Text2Obj", "txt", import_romtext)
