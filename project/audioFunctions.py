import numpy as np
import scipy.io.wavfile as scipy
import math
import numpy as np
import wave
import contextlib
from aubio import source, tempo

# Running mean supports audioPass
def running_mean(x,N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

# Wave file interpretation
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

# Modifies existing audio for high or low pass filter.
def audioPass(filePath, sampleRate, cutOffFrequency = 1000.0, hPass = False):

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
        
        if (hPass):
            for i in range(len(filtered)):
                filtered[i] = channels[0][i] - filtered[i]
        
        wav_file = wave.open(filePath, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()

# Parses Audio
def parseSongWav(pathInput):
    sampleRate, data = scipy.read(pathInput)    
    if (data.ndim == 2):
        data = data[:,0]
    box = np.array_split(data,8)

    bpm = 0
    s = source(pathInput, sampleRate, bpmH := 512)
    o = tempo("specdiff", bpmW := bpmH*2, bpmH, sampleRate)
    beats = []
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < bpmH:
            break
        
    if len(beats) > 1:
        bpm = np.median(60./np.diff(beats))
    tempData = np.array(data)
    return box, sampleRate, bpm, tempData

# Divides audio into 8 segments
def writeSong(pathInput, pathOutput, fName, passState = 0, speedMultiplier = 1.0, fractional = 1.0):
    parsedSong, sampleRate, bpm, data = parseSongWav(pathInput + fName)
    print(bpm, "BPM Analyzed")
    sampleRate = int(sampleRate*speedMultiplier)
        
    _fName = pathOutput + str(9) + fName
    scipy.write(_fName, sampleRate, data[:int(len(data)*fractional)])
    if (passState == 1):
        audioPass(_fName,sampleRate,500.0,False)
    elif (passState == 2):
        audioPass(_fName,sampleRate,3000.0,True)
            
            
            
    for i in range(len(parsedSong)):
        _fName = pathOutput + str(i+1) + fName
        scipy.write(_fName, sampleRate, parsedSong[i][:int(len(parsedSong[i])*fractional)])
        if (passState == 1):
            audioPass(_fName,sampleRate,500.0,False)
        elif (passState == 2):
            audioPass(_fName,sampleRate,3000.0,True)
