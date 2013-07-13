from morsealphabet import *
from constants import *

class MorseStream(object):
    def __init__(self):
        self.signals = []
        self.charBuffer = []
        self.wordBuffer = []
        self.sentenceBuffer = []
        
        self.morseAlphabet = MorseAlphabet()
    
    def add(self, signal):
        if signal == SHORT_PAUSE:
            return
        if signal in [SHORT, LONG]:
            self.signals.append(signal)
            return
        
        if signal == MEDIUM_PAUSE:
            character = self.morseAlphabet.getCharacter(self.signals)
            self.charBuffer.append(character)
            self.signals = []
            print(character)