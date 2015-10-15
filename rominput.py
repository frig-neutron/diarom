#!/usr/bin/env python
"""Read and index words from string"""

import rommodel

class ROMParseResult:
  indexedInput=''

class ROMInputParser: 
  def __init__(self): 
    self.wordCount=0

  def parse_words(self, words):
    """ Convert word string to list of ROMObject. 

    OID numbering spans invocations. The first OID returned will be one greater
    than the last OID of the previous invocation.  """
    oldWordCount = self.wordCount
    class ParseContext:
      def __init__(ctx):
        ctx.words=[]
        ctx.inWord=False
        ctx.word=''

    ctx=ParseContext()

    def next_word():
      self.wordCount+=1
      romobject = rommodel.ROMObject(ctx.word, self.wordCount)
      ctx.words+=[romobject]

    for c in words:
      if c.isalnum():
        ctx.word+=c
        ctx.inWord=True       
      else:
        if ctx.inWord:
          # end of word
          next_word()
        ctx.inWord=False
        ctx.word=''
    if ctx.inWord:
      next_word()

    return ctx.words

def read_file(path):
  """Convert all words in file to ROMObjects"""
  f = open(path)
  parser = ROMInputParser()
  wordlists = [parser.parse_words(line) for line in f]
  return reduce(list.__add__, wordlists)
