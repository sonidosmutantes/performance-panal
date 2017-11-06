import platform
from AudioServer import AudioServer 

import os
import OSC

class SupercolliderServer(AudioServer):
    # volume = 0.
    # pan = 0.
    # dry = 1.
    # wet = 0.
    # pyo_server = None

    def __init__(self):
        # TODO: implement MIDI support        
        # notes = Notein(poly=10, scale=1, mul=.5)
        # p = Port(notes['velocity'], .001, .5)
        pass
    #()

    def start(self, IP="127.0.0.1", port=57120):
        self.sc_IP = IP
        self.sc_Port = port
    #start()

    def set_amp(self, new_value):
        raise NotImplementedError
    #()
    def set_pan(self, new_value):
        raise NotImplementedError
    #()
    def set_reverb_config(self, dry=1., wet=0.):
        raise NotImplementedError
    #()
    def set_reverb_dry(self, dry):
        raise NotImplementedError
    #()
    def set_reverb_wet(self, wet):
        raise NotImplementedError
    #()

    def granular_synth(self, new_file, dry_value=1.):
        raise NotImplementedError
    #()

    def playfile(self, new_file, dry_value=1., loop_status=True):
        self.freeze_playfile(new_file)
    #()

    def freeze_playfile(self, new_file, dry_value=1., loop_status=True):
        """
            default synth (freeze)
        """

        # OSC Client (i.e. send OSC to SuperCollider)
        osc_client = OSC.OSCClient()

        # Virtual Box: Network device config not in bridge or NAT mode
        # Select 'Network host-only adapter' (Name=vboxnet0)
        # sc_IP = '192.168.56.1' # Remote server is the host of the VM
        osc_client.connect( ( self.sc_IP, self.sc_Port ) )

        print("\tPlaying %s/%s"%(os.environ["PWD"],new_file))
        msg = OSC.OSCMessage()
        msg.setAddress("/playfreeze") # (file,voice_number)
        msg.append( "%s/%s"%(os.environ["PWD"],new_file) )
        msg.append( self.enabled_voice-1) #convert to [0..7] range

        try:
            osc_client.send(msg)
        except Exception,e:
            print(e)
        #TODO: get duration from msg (via API)
        # time.sleep(duration)
        #()
#class