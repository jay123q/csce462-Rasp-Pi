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



