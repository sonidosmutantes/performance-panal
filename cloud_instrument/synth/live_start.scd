/*
    Sounds from the web (using API-Cultor) by hordia

    init & setup
*/

s.options.sampleRate= 48000; //traktor 2
//TODO: probar salida simultánea headphones + MAIN


s.boot; //start server



/*
// .wav record
thisProcess.platform.recordingsDir//locate folder
s.recHeaderFormat;//request default format
s.recHeaderFormat = "wav";
//s.recHeaderFormat = "aiff";
s.record;
s.stopRecording;
*/

s.waitForBoot {
	~bufferinstances = Array.newClear(8);
	~synthInstances = Array.newClear(8);

	//freeze ----> initial vol = 0
	SynthDef(\mutantefreeze, { arg out=0, bufnum=0, point=0, vol=0, fftwidth=4096, pan=0, startPos=0;
		var in, chain, sig;
		in = PlayBuf.ar(1, bufnum, BufRateScale.kr(bufnum),loop: 1);
		chain = FFT(LocalBuf(4096), in);
		chain = PV_MagFreeze(chain, point);

		//with PAN
		sig = Splay.ar(vol * IFFT(chain).dup);
		sig = Balance2.ar(sig[0], sig[1], pan);
		Out.ar(out, sig);
	}).add;

	//granular synth / grain synthesis
	SynthDef(\sfgrain, {arg bufnum=0, pan=0.0, startPos=0.0, amp=0.1, dur=0.04;
		var grain;

		grain= PlayBuf.ar(1,bufnum, BufRateScale.kr(bufnum), 1, BufFrames.ir(bufnum)*startPos, 0)*(EnvGen.kr(Env.perc(0.01,dur),doneAction:2)-0.001);

		Out.ar(0,Pan2.ar(grain, pan))}
	).add;


	//OSC function freeeze synth instance
	x = OSCFunc(
		{ | msg, time, addr, port |
			var new_file, voice_number;

			new_file = msg[1].asString;
			voice_number = msg[2].asInt;
			("Voice number: "+voice_number).postln;
			( "New sound received " + new_file ).postln;

			~bufferinstances[voice_number].free;
			~bufferinstances[voice_number] = Buffer.read(s, new_file);

			~synthInstances[voice_number].free;
			~synthInstances[voice_number] = Synth(\mutantefreeze, [\bufnum, ~bufferinstances[voice_number].bufnum, \out, 0, \vol, 0])
		},

		'/playfreeze'
	);
//x.free;

	////////////////
	//MIDI controller
	////////////////

	~mpkmidimix = AkaiMidiMix(); //también hace el midi connect All

	/////////////////////////////////////
// MIDI out

~default_channel = 0;
~midi_device_set_color = MIDIOut.newByName("MIDI Mix", "MIDI Mix");
~button_light = {
	|button_arg, onoff_arg|
	~midi_device_set_color.noteOn(~default_channel, button_arg, onoff_arg);
};

//Turn off all the buttons light
~mpkmidimix.recpads.do {|pad, i|
	~button_light.value(pad.note, 0); //off
};
~mpkmidimix.mutepads.do {|pad, i|
	~button_light.value(pad.note, 0); //off
};

~button_blink = {
   |button_arg|
	a = Task({
   ~button_light.value(button_arg, 1);
	0.2.wait;
   ~button_light.value(button_arg, 0);
	});
	a.start;
};

/////////////////////////////////////

	//master sound server volume (SuperCollider in DB)
	v = s.volume;
	~mpkmidimix.master[0].onChange = {|val| v.volume = val.linlin(0, 127, v.min, v.max) };
	~maxvol = 4;

	~mpkmidimix.recpads.do {|pad, i|
		pad.onPress = {|val|
			("REC ARM "+(i+1)).postln;
			~tmpsynth = ~synthInstances[i];
			~tmpsynth.get(\point, { arg value;
				if( value >0,{ //on (0 off,  >0 on)
					~tmpsynth.set(\point, 0);
					("MutanteSynth"+(i+1)+": Freeze OFF").postln;
					~button_light.value(pad.note, 0); //off
				}, {
					~tmpsynth.set(\point, 1);
					("MutanteSynth"+(i+1)+": Freeze ON").postln;
					~button_light.value(pad.note, 1); //on
				});
			});
		};
	};



	~granularAmount = [50,50,50,50,50,50,50,50]; //default values
	~granular_voladjust = 10;
	~mpkmidimix.mutepads.do {|pad, i|
		pad.onPress = {|val|
			"Granular synth Pad %\n".postf(i+1);

			~button_blink.value(pad.note);
			{
				('Granular amount '++~granularAmount[i] ).postln;
				~granularAmount[i].do{ arg j;
					var timeprop = (j/199.0)**3;
					Synth(\sfgrain,[\bufnum,  ~bufferinstances[i].bufnum, \startPos,rrand(0.0,timeprop),\amp, exprand(0.005,0.1)+~granular_voladjust, \pan, 1.0.rand2]);
					rrand((timeprop*0.1).max(0.01),timeprop*0.4).wait
				};
			}.fork
		};
	};

	~mpkmidimix.knobsA.do {|knob, i|
		//knob.onChange = {|val| ('~granular'++(i+1)++'_amount = '++ val.linlin(0,127,5,500)).interpret };
		knob.onChange = {|val| ~granularAmount[i] = val.linlin(0,127,5,500).asInteger };
	};

	~mpkmidimix.knobsC.do {|knob, i|
		knob.onChange = {|val| ~synthInstances[i].set(\pan, val.linlin(0,127,-1,1))};
	};

	//Sliders --> mutantefreeze_synth volume
	~mpkmidimix.sliders.do {|slider, i|
		slider.onChange = {|val| ~synthInstances[i].set(\vol, val.linlin(0,127,0,~maxvol))};
	};

	//Knobs --> mutantefreeze_synth PAN
	~mpkmidimix.knobsC.do {|knob, i|
		knob.onChange = {|val| ~synthInstances[i].set(\pan, val.linlin(0,127,-1,1))};
	};

} //end of waitForBoot