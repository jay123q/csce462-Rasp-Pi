def parseSongOLDFAILED(songPath):
    '''THIS IS OUTDATED might make a bin file for it later'''
    '''wav->mp3'''
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

def writeNewSongsOLD(filePathtoParsedSongs, parsedSong, sampleRate):
    '''old binary write using mp3 -> wav'''
    for i in range(len(parsedSong)):

        fileName = filePathtoParsedSongs + 'songPart'+str(i) + '.wav'
        parsedSongNumpy = np.array(parsedSong[i])
        parsedSongNumpy = parsedSongNumpy.astype('<U32')
        headerAddPart = np.concatenate((header.astype('<U32'),parsedSongNumpy), axis=0)
        headerAddPart = headerAddPart.astype('float32')
        #headerAddPart = convert_bytearray_to_wav_ndarray(headerAddPart)
        mem_buf = io.BytesIO( ) # we are converting to a mp3 then back to wav
        mem_buf.name = (fileName)
        sf.write( mem_buf, headerAddPart, fr, format='WAV' )
        mem_buf.seek( 0 )
        data, samplerate = sf.read(mem_buf)
        #fileName = filePathtoParsedSongs + 'songPart'+str(counter) + '.wav'
        p_data = sf.write(fileName, data , samplerate, subtype='PCM_16')