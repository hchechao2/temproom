import pyaudio
import wave
import os
# import sys

def play(username,num):
    CHUNK = 1024
    if os.path.isfile(username+'_'+str(num)+'.wav'):

        wf = wave.open(username+'_'+str(num)+'.wav', 'rb')
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

        print('play succeed')
    else:
        pass

if __name__=='__main__':
    play('admincbh')
