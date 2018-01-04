import pyaudio
import wave
import os
# import sys

def play(username):
    CHUNK = 1024
    if os.path.isfile(username+'.wav'):
        wf = wave.open(username+'.wav', 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != b'':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()
    else:
        print('no file to play')

if __name__=='__main__':
    play('admincbh')
