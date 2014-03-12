#!/usr/bin/env python

class ROMParseResult:
  words=[]
  indexedInput=''

def rom_parse_words(words):
  class ParseContext:
    words=[]
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

def rom_object_gen(data, string):
  import dia
  boxType=dia.get_object_type("Flowchart - Box")
  layer=data.active_layer

  parsed=rom_parse_words(string)
  for word in reversed(parsed.words):
    box, h1, h2=boxType.create(0,0)
    box.properties['text'] = word
    layer.add_object(box)

  dia.active_display().add_update_all()
  dia.active_display().flush()

def rom_object_gen_run(data, flags):
  rom_object_gen(data, """Develop a system to aid with recruiting, organizing and retaining cruise ship personnel. 
  The system should support categorization of opening and candidates using tags. Tags should be reusable and specific. Users should be able to update tags.
  The system should be accessible over the web on mobile devices. 
  The system should use the clients' preferred flavour of industry terminology.
  The system should support secure interaction with non-client personnel, including candidates and MDs. Some functions of system require that the user logs in with an account, other functions should be openly available.
  MDs should be able to input periodical onboard ratings directly on the web. This is to replace to the current system where MDs submit periodical onboard ratings via PDF or email, requiring manual data-entry.
  The system should support publishing openings on the web. Candidates accessing the system with a user account should be able to request assignments by sending Musician Contract Management Forms (MCMF). Candidates should be able to submit promotional packages through the system. Registered candidates should have access to a 'refer-a-friend' function.
  The client should be able to notify candidates of upcoming assignments through the system. 
  The system should support rich candidate profiles. Candidate profiles can contain links to web materials such as HeadHunter PromoPacks,  EPKs, and YouTube videos, periodical onboard MD ratings, and whether the candidate has an agent or not. The candidate profile should aid the client in tracking the candidates' position in the staffing process, from application on. Example statuses include 'applied' and 'evaluated'. Candidate profiles should include contracting-related attributes.
  The system should support staffing status reports. Staffing reports should enable the customer to determine current and future staffing on-board each ship. Staffing rosters should be partitionable by agency responsible for employee. The reports should provide information on amount paid to out to each agency.
  The system may import basic personnel information from various data sources, such as the 'Crew Manning System', which is a Human Resource tool at Carnival, and an in-house database colloquially referred to as 'the Access database'.
  """)

if __name__ == '__main__':
  pass
else:
  import dia
  dia.register_action ("DialogsGroupproperties", "ROM Object Generate", "/DisplayMenu/Dialogs/DialogsExtensionStart", rom_object_gen_run)
