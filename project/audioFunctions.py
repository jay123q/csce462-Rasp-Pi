import numpy as np
import scipy.io as scipy
import math
import numpy as np
import wave
import contextlib

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
        
def highPass(filePath, sampleRate, cutOffFrequency = 1000.0):

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

        # Use moving average (only on first channel)
        print(channels[0], len(channels[0]))
        print("--------------------------")
        filtered = running_mean(channels[0], N).astype('int16')
        print(filtered, len(filtered))
        
        for i in range(len(filtered)):
            filtered[i] = channels[0][i] - filtered[i]
        
        '''
        Subtract origin signal from low pass signal = high pass signal.
        https://gist.github.com/piercus/b005ed5fbc70761bde96
        high_filtered = channels[0] - filteredd
        '''
        
        wav_file = wave.open(filePath, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()

def lowPass(filePath, sampleRate, cutOffFrequency = 1000.0):
    
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

def parseSongWav(pathInput):
    sampleRate, data = scipy.wavfile.read(pathInput)    
    if (data.ndim == 2):
        data = data[:,0]
    box = np.array_split(data,8)
    return box, sampleRate

def writeSong(pathInput, pathOutput, passState = 0, speedMultiplier = 1.0):
    parsedSong, sampleRate = parseSongWav(pathInput)
    sampleRate = int(sampleRate*speedMultiplier)
    for i in range(len(parsedSong)):
        fName = pathOutput + str(i+1) + '.wav'
        scipy.wavfile.write(fName, sampleRate, parsedSong[i])
        if (passState == 1):
            lowPass(fName,sampleRate,500.0)
        elif (passState == 2):
            highPass(fName,sampleRate,1000.0)
