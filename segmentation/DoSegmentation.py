#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
# from cache import memoize # TODO: add dependecy
import numpy as np
import essentia
from essentia.standard import *
from random import choice
import os

# @memoize
def do_segmentation(audio_input, audio_input_from_filename = True, audio_input_from_array = False, sec_len = 6, save_file = True):

    lenght = int(sec_len) * 10

    if audio_input_from_filename == True:                                           
        x = MonoLoader(filename = audio_input)()
        print(audio_input)
    if (audio_input_from_filename == False) and audio_input_from_array == True:                                           
        x = audio_input

    frames_duration = Duration()

    frame_size = 4096

    hop_size = 1024
 
    segments = [frames_duration(frame) for frame in FrameGenerator(x, frameSize=frame_size, hopSize=hop_size)]

    output = []
    for segment in segments:                                           
        sample = segment*44100 
        output.append(x[:sample*lenght]) #extend duration of segment

    output = choice(output)                                           

    if save_file == True:                                          
        baseName = os.path.splitext(audio_input)[0].split('/')[-1]                                                                       
        outputFilename = 'samples'+'/'+baseName+'_sample'+'.wav'                                                       
        print("output: "+outputFilename)
        MonoWriter(filename = outputFilename)(output)
        print("File generated: %s"%outputFilename)
    if save_file == False:
        return output

# ext_filter = ['.wav', '.mp3'] #valid audio files
ext_filter = ['.wav'] #valid audio files

Usage = "./DoSegmentation.py [FILES_DIR]"
#Output: outputFilename = 'samples'+'/'+baseName+'_sample'+'.wav'        
if __name__ == '__main__':
  
    if len(sys.argv) < 2:
        print "\nBad amount of input arguments\n", Usage, "\n"
        sys.exit(1)


    # segment_length = 6
    segment_length = 10
    # try:
    files_dir = sys.argv[1] 

    if not os.path.exists(files_dir):                         
        raise IOError("Must download sounds")

    for subdir, dirs, files in os.walk(files_dir):
        for f in files:
            # print(f)
            if not os.path.splitext(f)[1] in ext_filter:
                continue
            audio_input = subdir+'/'+f
            do_segmentation( audio_input, audio_input_from_filename = True, audio_input_from_array = False, sec_len = segment_length, save_file = True)

    # except Exception, e:
    #     print(e)
    #     exit(1)
