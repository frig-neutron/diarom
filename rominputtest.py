#!/usr/bin/env python
import unittest
import rominput

class DiaRomTest(unittest.TestCase):
  def test_twoWordsInOneCallShouldHaveOids(self):
    parser = rominput.ROMInputParser()

    romObjects = parser.parse_words("one two")
  
    self.assertEqual(romObjects[0].oid, 1)
    self.assertEqual(romObjects[1].oid, 2)

  def test_twoWordsInOneCallShouldHaveTextLabels(self):
    parser = rominput.ROMInputParser()

    romObjects = parser.parse_words("one two")
  
    self.assertEqual(romObjects[0].text, "one")
    self.assertEqual(romObjects[1].text, "two")
    
  def test_parserShouldRememberObjectIndexBetweenCalls(self):
    parser = rominput.ROMInputParser()

    romObjects = parser.parse_words("throwaway")
    romObjects = parser.parse_words("keeper")

    self.assertEqual(romObjects[0].oid, 2)
  
if __name__ == '__main__':
  unittest.main()
