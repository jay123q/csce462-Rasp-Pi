import math
import numpy as np
import wave
import contextlib


def wavePass(filePath, sampleRate, highPass, lowPass):  

  if(lowPass == 1):
    cutOffFrequency = 1000.0
    # from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    
    def running_mean(x,N):
        cumsum = np.cumsum(np.insert(x, 0, 0)) 
        return (cumsum[N:] - cumsum[:-N]) / float(N)
    
    def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

        if sample_width == 1:
            dtype = np.uint8 # unsigned char
            2
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
        #print(type(filtered))
        '''
        
        the idea is that you can subtract the original signal from the low pass signal and get a 
        high pass! pretty simple fix but ive hit a wall with debugging. Below is the reference
        i used th find the above information as well as some sample code (buggy) I typed up.
        
        https://gist.github.com/piercus/b005ed5fbc70761bde96
        high_filtered = channels[0] - filtered
        
        '''
  if(highPass == 1):
            for i in range(len(filtered)):
                filtered[i] = channels[0][i] - filtered[i]
        
  wav_file = wave.open(filePath, "w")
  wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
  wav_file.writeframes(filtered.tobytes('C'))
  wav_file.close()        

'''
DEPRECATED FUNCTIONS

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def convert_bytearray_to_wav_ndarray(input_bytearray: bytes, sampling_rate=44100):
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sampling_rate, np.frombuffer(input_bytearray, dtype=np.int16))
    output_wav = byte_io.read()
    output, samplerate = sf.read(io.BytesIO(output_wav))
    return output


def parseSongOLDFAILED(songPath):
    ''''''THIS IS OUTDATED might make a bin file for it later'''''''
    wf = wave.open(songPath, 'rb')
    #nchan = wf.getparams().nframes
    #swidth = wf.getparams().sampwidth
    fr = wf.getparams().framerate
    bin_data = wf.readframes(wf.getparams().nframes)

    bd = []
    for my_byte in bin_data:
      bd.append(f'{my_byte:0>8b}')

    countHeaderIndex = 0
    parsedHeader = np.array([])

    for i in range(len(bd)):
        if(countHeaderIndex > 43):
            break
        else:
            countHeaderIndex+=1
            parsedHeader = np.append(parsedHeader,bd[i])

    countPosRemove = 0

    parsingIndex = (len(bd) - 44 ) /8 # 8 buttons
    parsingKeyCount=0
    dictKeyIndex = 0

    partSongs = {0: [],1 : [],2:[],3:[],4:[],5:[],6:[],7:[]}
    for i in range(44,len(bd)):
            if(parsingIndex < parsingKeyCount):
                dictKeyIndex +=1
                parsingKeyCount = 0
            partSongs[dictKeyIndex].append( bd[i])
            parsingKeyCount+=1

    return partSongs,fr,parsedHeader

'''



