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

