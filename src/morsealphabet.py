from constants import *

class MorseAlphabet(object):
    def __init__(self):
        self.alphabet = \
                {
                 'S': [SHORT, SHORT, SHORT],
                 'O': [LONG, LONG, LONG]
                 }
    
    def getCharacter(self, signalBuffer):
        for key, value in self.alphabet.items():
            if signalBuffer == value:
                return key
        
        return ''