#!/usr/bin/env python
"""Read and index words"""

class ROMParseResult:
  words=[]
  indexedInput=''

class ROMInputParser: 
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
