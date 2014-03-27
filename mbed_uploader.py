#!/usr/bin/env python

#description      A short script to monitor a directory for .bin files and upload to MBED devices.
#author           Tomas Cerskus
#license          MIT

import sys
import time
import shutil
import ntpath
import os
from optparse import OptionParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

class MbedUploaderEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global options

        if type(event) is not FileModifiedEvent:
            return
        if not event.src_path.endswith(".bin"):
            return
        
        try:
            shutil.move(event.src_path, options.output_dir+ntpath.basename(event.src_path))
            if options.sound:
                from pygame import mixer
                mixer.init()
                alert=mixer.Sound('bell.wav')
                alert.play()
        except IOError as (errno, strerror):
            print "Failed to upload. Check that output directory is correct.";
            print "I/O error({0}): {1}".format(errno, strerror)

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_dir", default="~/Downloads/Chrome/",
                  help="directory to monitor for .bin files", metavar="FILE")
parser.add_option("-o", "--output", dest="output_dir", default="/media/NUCLEO/",
                  help="directory to upload .bin files", metavar="FILE")
parser.add_option("-s", "--sound",
                  action="store_true", dest="sound", default=False,
                  help="play a sound after successful upload")

(options, args) = parser.parse_args()

#observer.schedule does not recognise ~ symbol
options.input_dir = os.path.expanduser(options.input_dir)

#
options.input_dir = os.path.abspath(options.input_dir)
options.output_dir = os.path.abspath(options.output_dir)

print 'Monitoring "' + options.input_dir + '".'
print 'Going to upload to "' + options.output_dir + '".'
print 'Sound is ' + 'on' if options.sound else 'off' + '.'


if __name__ == "__main__":
    event_handler = MbedUploaderEventHandler()
    observer = Observer()
    observer.schedule(event_handler, options.input_dir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
