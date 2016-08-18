#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pykov # Markov chains helpers
import time
import random
import urllib2
import OSC

# RedPanal API
URL_BASE = "http://127.0.0.1:5000" #TODO: get from a config file

# OSC Server
osc_client = OSC.OSCClient()
#Local SC server
osc_client.connect( ( '127.0.0.1', 57121 ) )
#Remote server
#osc_client.connect( ( '10.142.39.109', 57120 ) )
#Virtual Box: Network Adapter in NAT mode (not bridge)
osc_client.connect( ( '10.0.2.3', 57120 ) ) #internal network with host OS

# 3 states  (each row must sum 1)
# idle -> no sound
# harmonic -> choose one harmonic sound (or note) from database with a given frec and time?
# inharmonic

T = pykov.Matrix()

T['idle','harmonic'] = .2
T['idle','inharmonic'] = .1
T['idle','idle'] = .7

T['harmonic','idle'] = .2
T['harmonic','inharmonic'] = .1
T['harmonic','harmonic'] = .7

T['inharmonic','idle'] = .9
T['inharmonic','inharmonic'] = .1
#T['inharmonic','inharmonic'] = 0


try:
    T.stochastic() #check
except Exception,e:
    print(e)
    exit(1)


duration = 1 #FIXME: hardcoded
time_bt_states = 1 # (delay within states...)
state = 'idle' #start state

events = 10 # or loop with while(1)
# for i in range(events):
while(1):
      print( state ) # TODO: call the right method for the state here
      if state=='harmonic':
        call = '/list/samples' #gets only wav files because SuperCollider
        response = urllib2.urlopen(URL_BASE + call).read()
        audioFiles = list()
        for file in response.split('\n'):
            if len(file)>0: #avoid null paths
                audioFiles.append(file)
                # print file
        file_chosen = audioFiles[ random.randint(0,len(audioFiles)-1) ]
        print("\tPlaying %s"%file_chosen)
        msg = OSC.OSCMessage()
        msg.setAddress("/play")

        #mac os
        msg.append( "/Users/hordia/Documents/apicultor"+file_chosen.split('.')[1]+'.wav' )

        try:
            osc_client.send(msg)
        except Exception,e:
            print(e)
        #TODO: get duration from msg (via API)
        time.sleep(duration)


      state = T.succ(state).choose() #new state
      time_between_notes = random.uniform(0.,2.) #in seconds
      time.sleep(time_between_notes)
      #delay within states
      time.sleep(time_bt_states)
