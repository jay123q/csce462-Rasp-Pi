import math
import numpy as np
import wave
import contextlib
def lowPass(filePath, sampleRate):  
    '''
    
    Yo! I found some code that does a pretty solid low pass on stack overflow i just
    modified it to meet our parameters. I've set the lowpass pretty agressively to cut everything
    above 400 hz, so youll basically only here the thumping of the bass and some misc percussive
    sounds!
    
    I liked this solution the best since it does everything "in house" with the imports,
    so no black boxes! no sirrr!
    
    High pass CAN be reverse engineered from the low pass but im hitting a wall with debugging rn.
    
    -Brown
    '''
    cutOffFrequency = 1000.0
    # from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def running_mean(x,N):
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        return (cumsum[N:] - cumsum[:-N]) / float(N)
    
    def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

        if sample_width == 1:
            dtype = np.uint8 # unsigned char
            
        elif sample_width == 2:
                dtype = np.int16 # signed 2-byte short
                
        else:
                raise ValueError("Only supports 8 and 16 bit audio formats.")

        channels = np.fromstring(raw_bytes, dtype=dtype)

        if interleaved:
            # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
            channels.shape = (n_frames, n_channels)
            channels = channels.T
        else:
            # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
            channels.shape = (n_channels, n_frames)

        return channels  
    
    with contextlib.closing(wave.open(filePath,'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        # Extract Raw Audio from multi-channel Wav File
        signal = spf.readframes(nFrames*nChannels)
        spf.close()
    
        channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

        # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        freqRatio = (cutOffFrequency/sampleRate)
        N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)
        #print(N)
        # Use moving average (only on first channel)
        filtered = running_mean(channels[0], N).astype('int16')
        
        '''
        Subtract origin signal from low pass signal = high pass signal.
        https://gist.github.com/piercus/b005ed5fbc70761bde96
        high_filtered = channels[0] - filteredd
        '''
        
        wav_file = wave.open(filePath, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()