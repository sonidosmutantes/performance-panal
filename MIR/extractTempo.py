#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import numpy as np
import scipy
from essentia import *
from essentia.standard import *

ext_filter = ['.mp3','.ogg','.ogg','.wav']

def process_file(inputSoundFile, frameSize = 1024, hopSize = 512):
    input_signal = MonoLoader(filename = inputSoundFile)()
    sampleRate = 44100 #FIXME
    
    
    #filter direct current noise
    offset_filter = DCRemoval() 
    timelength = Duration() 
    bpm = RhythmExtractor2013()

    audio = offset_filter(input_signal)
    beatsperminute, ticks = bpm(audio)[0], bpm(audio)[1]
#   pool.add(desc_name, beatsperminute)
#   pool.add('rhythm.bpm_ticks', ticks)
    # print( "BPM: %i, ticks: %i"%(beatsperminute,ticks) )
    print("BPM: %f"%beatsperminute)

    duration = timelength(audio)
    print("Duration: %f"%duration)

#()    

#Usage = "./run_MIR_analysis.py [FILES_DIR]"
if __name__ == '__main__':
  
    if len(sys.argv) < 2:
        print "\nBad amount of input arguments\n\t", Usage, "\n"
#        print("Example:\n\t./run_MIR_analysis.py data\n\t./run_MIR_analysis.py samples\n")
        sys.exit(1)


    try:
        f = sys.argv[1] 

#        if not os.path.exists(files_dir):                         
#            raise IOError("Must download sounds")

        if not os.path.splitext(f)[1] in ext_filter:
            raise Exception

        process_file( f )
    except Exception, e:
        print(e)
        exit(1)
