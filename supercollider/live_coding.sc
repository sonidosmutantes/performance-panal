s.boot; //start server
//s.quit; //stops server

~ip.postln; //apicultor ws ip

Buffer.freeAll; // no sound

MIDIIn.connectAll;

//function
	f = { arg a, b = 2; a + b; };
	a = f.value(2);
    a;

r = Synth(\playBufMono, [\bufnum, ~bank1a.bufnum, \rate, 0.5]); //buffer a at half speed
r = Synth(\playBufMono, [\bufnum, ~bank1a.bufnum, \rate, 1, \out, 3]); //buffer full speed
r = Synth(\playBufMono, [\bufnum, a.bufnum, \rate, 0.5]); //buffer a at half speed

r = Synth(\mutantefreeze, [\bufnum, a.bufnum, \rate, 1]); //

//g =Buffer.read(s, "/Users/hordia/Documents/vmshared/samples/Cuesta_caminar_batero_sample2.wav" );
i=Buffer.read(s, "/Users/hordia/Documents/vmshared/samples/1291_sample2.wav" );
r = Synth(\playBufMono, [\bufnum, i.bufnum, \rate, 0.5]); //buffer a at half speed
-------

//Panning
		LinPan2.ar(in, pos, level);
		LinPan2.ar(in, -1, 1);

play({ LinPan2.ar(PinkNoise.ar(0.4), FSinOsc.kr(2)) }); //oscilating pink noise

SynthDef("help-LinPan2", {  Out.ar(0, LinPan2.ar(FSinOsc.ar(800, 0, 0.1), FSinOsc.kr(3))) }).play;

// You'll only hear the front two channels on a stereo setup.
(
SynthDef("help-Pan4", {
    Out.ar(0, Pan4.ar(PinkNoise.ar, FSinOsc.kr(2), FSinOsc.kr(1.2), 0.3))
}).play;
)

play({ Pan4.ar(PinkNoise.ar, -1,  0, 0.3) }); // left pair
play({ Pan4.ar(PinkNoise.ar,  1,  0, 0.3) }); // right pair
play({ Pan4.ar(PinkNoise.ar,  0, -1, 0.3) }); // back pair
play({ Pan4.ar(PinkNoise.ar,  0,  1, 0.3) }); // front pair

play({ Pan4.ar(PinkNoise.ar,  0,  0, 0.3) }); // center
----
	//function mutante freeze synth (in mute mode, volumen = 0
	~prepare_freeze = { arg buf, f_chan, bank, letter;
				//format("% / % / mute vol=0", bank, letter).postln;
                Synth(\mutantefreeze, [\bufnum, buf, \out, f_chan, \vol, 0]);
	};

	//función invierte el valor de freeze
	~invert_freeze = { arg freeze_x, bank, letter;
		freeze_x.get(\point, { arg val;
				if( val >0,{ //on (0 off,  >0 on)
			 		freeze_x.set(\point, 0);
					format("% / % / freeze OFF", bank, letter).postln;
	    		}, {
					freeze_x.set(\point, 1);
					format("% / % / freeze ON", bank, letter).postln;
			    });
			});
	};
----
//loop and freeze del sonido 3(c)
volumenes y parametros
				z.set(\vol, 0);
        z.set(\vol, 1);
z.set(\vol, 2);
z.set(\vol, 3);
//z.set(
//-----
// **** Get new sound, fill de buffer and  play ***

//Get a new sample in a new buffer
		        //Get a new sample file from apicultor
		        format("curl http://%:5000/list/samples -o desc.tmp", i).unixCmd; //mac os
		       //FIXME: wait to download here? (takes effect next time)

		        f = FileReader.read("./desc.tmp".standardizePath); //array
		        m = 10; //Length of sound list (TODO: retrieve from API) FIXME
		        v = f.at(m.rand)[0]; //select a random value from array (0..10 range)
		        v.postln(); //selected file
		        f = ("/Users/hordia/Documents/vmshared"+v.replace("./","/")).replace(" ",""); //trim spaces (TODO: check why there is an extra space in the path)
		        d = Buffer.read(s, f );


		        //plays new sample
				r = Synth(\playBufMono, [\out, 0, \bufnum, d.bufnum, \rate, 1]); //d
				r = Synth(\playBufMono, [\out, 1, \bufnum, d.bufnum, \rate, 1]); //d

//------

// Monitor

//Mostrar MIDI input (controls)
MIDIIn.control = {arg src, chan, num, val;
	[chan,num,val].postln;
};

//Mostrar nota + velocity
MIDIFunc.noteOn({ |veloc, num, chan, src|
	( "New note received " + num + " with vel "+veloc ).postln;
});


//-----
//Trigger sound with pads

MIDIFunc.noteOn({ |veloc, num, chan, src|

	// * Bank1: Second ROW of pads *
	if(num == 44, {
		~invert_freeze.value(w, "Bank1", "A");
	});
	if(num == 45, {
		~invert_freeze.value(x, "Bank1", "B");
	});
	f(num == 46, {
		~invert_freeze.value(y, "Bank1", "C");
	});
    if(num == 19,{
		~invert_freeze.value(z, "Bank1", "D");
	});

});
