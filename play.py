import pyaudio
import wave
# import sys

def play(username):
    CHUNK = 1024
    print('playing1')
    try:
    	wf = wave.open(username+'.wav', 'rb')
    except:
    	return 0
    p = pyaudio.PyAudio()
    print('playing2')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    print('playing3')
    data = wf.readframes(CHUNK)
    print('playing4')
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__=='__main__':
    play('admincbh')
