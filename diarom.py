import dia

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

def rom_object_gen(string):
  boxType=dia.get_object_type("Flowchart - Box")
  layer=dia.diagrams()[0].data.active_layer

  parsed=rom_parse_words(string)
  for word in reversed(parsed.words):
    box, h1, h1=boxType.create(0,0)
    box.properties['text'] = word
    layer.add_object(box)

  dia.active_display().add_update_all()
  dia.active_display().flush()

def rom_object_gen_run(data, flags):
  rom_object_gen("""To make use of a business opportunity, the designer will design a house. 

The house can fly by moving using the air as the primary means of support. The house flies between flat ground areas within a volume with sufficient dimensions to accomodate the house and the physical effects of flying the house and having no objects within it or the space required for moving the house in or out of the area.

The house should be simple to fly by entering and executing a flight plan, abstract of unnecessary technical details. Entering and executing a flight plan is done by using a console-based user interface to enter a specification of a flight destination, intended air route, time of departure and arrival, and instructing the flight computer to execute.

The house takes off and lands vertically. At landing the house will ensure the ground site is clear, stop horizontal motion over the ground site, and slowly reduce altitude until contact with ground. At takeoff the house will ensure the exit route is clear and slowly increase altitude while keeping horizontal motion to zero.

The house will have a 200 km range.

The house will fly to effect ground change of scenery and nearby resources for the occupants. The provides shelter and comfort and facilitates recreation. The house provides shelter and comfort by acting as a physical barrier between the natural environtment and the occupants into an isolated internal environtment, and by granting access to food reserves, sanitation facilities, comfortable furniture, internal atmospheric temperature and pressure control.""")


dia.register_action ("DialogsGroupproperties", "ROM Object Generate", "/DisplayMenu/Dialogs/DialogsExtensionStart", rom_object_gen_run)



