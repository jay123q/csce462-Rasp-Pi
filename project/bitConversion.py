def bitstring_to_bytes(s):
    '''Rohan Function unused'''
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def convert_bytearray_to_wav_ndarray(input_bytearray: bytes, sampling_rate=44100):
    '''Rohan Function fix read'''
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io, sampling_rate, np.frombuffer(input_bytearray, dtype=np.int16))
    output_wav = byte_io.read()
    output, samplerate = sf.read(io.BytesIO(output_wav))
    return output



def fixNoise():
    '''Joshua function fix noise in wav'''