import pyaudio
import wave
import os
# import sys

def play(username):
    num=1
    CHUNK = 1024
    while 1:
        if os.path.isfile(username+str(num)+'.wav'):
            #print('play 1')
            wf = wave.open(username+str(num)+'.wav', 'rb')
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
            num +=1
            #print('play 2')
        else:
            print('no file to play')
            break
if __name__=='__main__':
    play('admincbh')
