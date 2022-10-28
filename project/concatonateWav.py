# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 21:55:39 2022

@author: Owner
"""
import numpy as np
import scipy.io.wavfile as scipy
import math
import numpy as np
import wave
import contextlib



import wave

infiles = ["drum.wav", "drum.wav","drum.wav", "drum.wav","drum.wav", "drum.wav","drum.wav","drum.wav", "drum.wav","drum.wav", "drum.wav","drum.wav", "drum.wav","drum.wav", "drum.wav","drum.wav"]
outfile = "drum2.wav"

data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()
    
output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
for i in range(len(data)):
    output.writeframes(data[i][1])
output.close()