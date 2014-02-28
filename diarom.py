def rom_object_create(words):
  class ParseContext:
    wordsIndexed=''
    wordCount=0
    inWord=False
    word=''
  ctx= ParseContext()

  def next_word():
    ctx.wordCount+=1
    sufx='['+str(ctx.wordCount)+']'
    ctx.word+=sufx
    ctx.wordsIndexed+=sufx

  for c in words:
    if c.isalnum():
      ctx.word+=c
      ctx.wordsIndexed+=c
      ctx.inWord=True       
    else:
      if ctx.inWord:
        # end of word
        next_word()
        print(ctx.word)
      ctx.inWord=False
      ctx.wordsIndexed+=c
      ctx.word=''
  if ctx.inWord:
    next_word()
    print(ctx.word)
  print ctx.wordsIndexed

rom_object_create('the cat shat on the mat')
