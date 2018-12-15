import pyaudio
import wave
import audioop
import aubio
import numpy as np
import Tester as t


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 50
WAVE_OUTPUT_FILENAME = "output.wav"

lastRms = 0
lastPitch = -55
BRI_MODIFIER = 15 #15
DIFFERENCE_THRESHOLD = 30

p = pyaudio.PyAudio()

# open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048,
    2048//2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

print("* recording")
#p
print(range(0, int(RATE / CHUNK * RECORD_SECONDS)))

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    #print("yo: ",audioop.avg(data, 2), rms)
        
    # difference between current volume and last volume
    #
    diff = rms - lastRms
    
    percentage = rms/100
        
    # checks if |diff| exceeds the difference_threshold
    if(abs(diff) >= DIFFERENCE_THRESHOLD):

        # sets the brightness value
        bri = int(BRI_MODIFIER * percentage)
        
        if(bri < 0):
            bri = 0
        elif(bri > 254):
            bri = 254
            
        print("Difference: ",diff,"\nBrightness: ", bri)
        t.change_bri(bri)
          

    lastRms = rms


print("* done")

stream.stop_stream()
stream.close()

p.terminate()