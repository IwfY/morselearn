#!/usr/bin/env python3

# dependencies:
# * python-gobject
# * gstreamer 1.0
# * gst-plugins-good (for autoaudiosink)

import sys
import time

from gi.repository import Gtk, Gdk, Gst

from constants import *
from morsealphabet import *
from morsestream import *

class MorseLearner(object):
    def __init__(self):
        self.window = None
        self.label = None
        
        self.actionPressed = False
        self.timePressed = None
        self.durationPressed = 0
        self.durationReleased = 0
        self.averagePressDuration = [0.15, 10]      # [average, count]
        self.averageReleaseDuration = [0.2, 10]
        
        self.morseStream = MorseStream()
        
        self.pipeline = None
        self.source = None
        self.sink = None
        
        self.setupWindow()
        self.setupAudioPipeline()
        Gtk.main()
    
    def setupWindow(self):
        self.window = Gtk.Window()
        self.window.connect('delete-event', Gtk.main_quit)
        self.window.connect('key_press_event', self.keyPressed)
        self.window.connect('key_release_event', self.keyReleased)
        
        self.label = Gtk.Label(label='press down arrow')
        
        self.window.add(self.label)
        
        self.window.show_all()
    
    def setupAudioPipeline(self):
        self.pipeline = Gst.Pipeline(name='audio')
        self.source = Gst.ElementFactory.make('audiotestsrc', 'src')
        self.sink = Gst.ElementFactory.make('autoaudiosink', 'output')
        
        self.pipeline.add(self.source)
        self.pipeline.add(self.sink)
        
        self.source.link(self.sink)


    def keyPressed(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == "Down":
            if not self.actionPressed:
                if not self.timePressed is None:
                    self.durationReleased = \
                            round(time.time() - self.timePressed, 2)
                    self.averageReleaseDuration = \
                            [(self.averageReleaseDuration[0] * \
                                    self.averageReleaseDuration[1] + \
                                    self.durationReleased) / \
                                    (self.averageReleaseDuration[1] + 1),
                             self.averageReleaseDuration[1] + 1]

                    print('average pause', self.averageReleaseDuration[0])
                    if self.durationReleased > self.averageReleaseDuration[0]:
                        self.morseStream.add(MEDIUM_PAUSE)

                self.timePressed = time.time()
                
                self.actionPressed = True
                self.source.set_property('freq', 350.0)
                self.pipeline.set_state(Gst.State.PLAYING)


    def keyReleased(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == "Down":
            self.durationPressed = round(time.time() - self.timePressed, 2)
            self.timePressed = time.time()
            self.averagePressDuration = \
                            [(self.averagePressDuration[0] * \
                                    self.averagePressDuration[1] + \
                                    self.durationPressed) / \
                                    (self.averagePressDuration[1] + 1),
                             self.averagePressDuration[1] + 1]

            if self.durationPressed <= self.averagePressDuration[0]:
                self.morseStream.add(SHORT)
            else:
                self.morseStream.add(LONG)
            
            self.pipeline.set_state(Gst.State.NULL)
            self.actionPressed = False
            

def main():
    Gst.init(sys.argv)
    m = MorseLearner()


if __name__ == '__main__':
    main()
