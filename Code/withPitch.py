import pyaudio
import wave
import audioop
import aubio
import numpy as np
import LightHandler as t
import time


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 55
WAVE_OUTPUT_FILENAME = "output.wav"

lastRms = 0
lastPitch = -55
lastColor = "nix"

BRI_MODIFIER = 18 #15
DIFFERENCE_THRESHOLD = 20

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
pDetection.set_tolerance(0.8)

print("* recording")
#p
print(range(0, int(RATE / CHUNK * RECORD_SECONDS)))

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    
    # for aubio, only works with float32, so we are gonna convert...
    data32 = np.fromstring(data, dtype=np.int16)
    data32 = data32.astype(np.float32,order='C') / 32768.0
    
    # aubio
    samples = np.fromstring(data32,
        dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    # Compute the energy (volume) of the
    # current frame.
    volume = (np.sum(samples**2)/len(samples))*1000
    # Format the volume output so that at most
    # it has six decimal numbers.
    volume = "{:.3f}".format(volume)
    
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    #print("yo: ",audioop.avg(data, 2), rms)
        
    # difference between current volume and last volume
    #
    diff = rms - lastRms
    color = "red"
    
    percentage = rms/100
    #percentage = diff/100
        
    # checks if |diff| exceeds the difference_threshold
    if(abs(diff) >= DIFFERENCE_THRESHOLD):

        # sets the brightness value
        bri = int(BRI_MODIFIER * percentage)
        
        if(bri < 0):
            bri = 0
        elif(bri > 254):
            bri = 254
            
        #print("Difference: ",diff,"\nBrightness: ", bri,"\nPitch: ",pitch,"Volume: ",volume)
        #t.change_bri(bri)
                        
        #if(bri >= 0 and bri <= 254):
    
  
    #if(abs(pitch - lastPitch) >= 15):
    if(pitch <= 2000 and True):
        print(pitch)     
        if(pitch <= 150 and pitch >= 0):
            color = "red"
        elif(pitch <= 300 and pitch >= 151):
            color = "orange"
        elif(pitch <= 450 and pitch >= 301):
            color = "yellow"
        elif(pitch <= 700 and pitch >= 451):
            color = "blue"
        elif(pitch >= 701):
            color = "purple"
        
        
    #if(pitch <= 2000 and True):
     #   print(pitch)     
      #  if(pitch <= 150 and pitch >= 0):
       #     color = "turq"
        #elif(pitch <= 300 and pitch >= 151):
         #   color = "blue"
       # elif(pitch <= 450 and pitch >= 301):
        #    color = "red"
        #elif(pitch <= 700 and pitch >= 451):
        #    color = "orange"
        #elif(pitch >= 701):
        #    color = "yellow"      
        
        if(color != lastColor):
            t.change_light(color,1)
            print("\n\tCOLOR CHANGED:\n",color,pitch)
            
        lastColor = color
        #print(color,pitch)
        
    lastRms = rms
    lastPitch = pitch
    
print("* done")

stream.stop_stream()
stream.close()

p.terminate()