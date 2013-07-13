#!/usr/bin/env python3

# dependencies:
# * python-gobject
# * gstreamer 1.0
# * gst-plugins-good (for autoaudiosink)

import sys
from gi.repository import Gtk, Gdk, Gst

class MorseLearner:
    def __init__(self):
        self.window = None
        self.button = None
        self.actionPressed = False
        
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
                self.actionPressed = True
                self.source.set_property('freq', 350.0)
                self.pipeline.set_state(Gst.State.PLAYING)
            
    def keyReleased(self, widget, event):
        key = Gdk.keyval_name(event.keyval)
        if key == "Down":
            self.pipeline.set_state(Gst.State.NULL)
            self.actionPressed = False
            

def main():
    Gst.init(sys.argv)
    m = MorseLearner()


if __name__ == '__main__':
    main()
