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
RECORD_SECONDS = 25
WAVE_OUTPUT_FILENAME = "output.wav"

lastRms = 0
lastPitch = -55
lastColor = "nix"
lastBri = 0
requestsSend = 0

BRI_MODIFIER = 18 #15
DIFFERENCE_THRESHOLD = 20 #20 #50
PITCH_COLORS_ON = True

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

print(range(0, int(RATE / CHUNK * RECORD_SECONDS)))

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    
    # for aubio, only works with float32, so we are gonna convert...
    #data32 = np.fromstring(data, dtype=np.int16)
    data32 = np.frombuffer(data, dtype=np.int16)
    data32 = data32.astype(np.float32,order='C') / 32768.0
    
    # aubio
    #samples = np.fromstring(data32, dtype=aubio.float_type)
    samples = np.frombuffer(data32, dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    
    # Compute the energy (volume) of the
    # current frame.
    #volume = (np.sum(samples**2)/len(samples))*1000
    
    # Format the volume output so that at most
    # it has six decimal numbers.
    #volume = "{:.6f}".format(volume)    
    
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    
   
    # difference between current volume and last volume
    diff = rms - lastRms
    color = "red"
    
    percentage = rms/100
       
    # checks if |diff| exceeds the difference_threshold
    if(abs(diff) >= DIFFERENCE_THRESHOLD):

        # sets the brightness value
        bri = int(BRI_MODIFIER * percentage)
        
        if(bri < 0):
            bri = 0
        elif(bri > 254):
            bri = 254
            
        #print("Difference: ",diff,"\nBrightness: ", bri,"\nPitch: ",pitch,"Volume: ",volume)
        if(PITCH_COLORS_ON==False):
            t.change_bri(bri)
        #requestsSend = requestsSend + 1

    
  
    #if(abs(pitch - lastPitch) >= 15):
    if(PITCH_COLORS_ON):
        if(pitch <= 1500):
            if(pitch <= 170 and pitch >= 0):
                color = "blue"
            elif(pitch <= 325 and pitch >= 171):
                color = "purple"
            elif(pitch <= 900 and pitch >= 326):
                color = "red"
            else:
                color = "yellow"
        else:
            color = "yellow"
        
        if(True): # To reduce requests...
            if(color != lastColor):
                t.change_light_and_bri(color,1,bri)
                #time.sleep(0.08)
                requestsSend = requestsSend +1
            else:
                if(lastBri != bri):
                    t.change_bri(bri)
                    #time.sleep(0.08)
                    requestsSend = requestsSend +1
        else: # Changes pitch color, but doesn't change bri
            if(color != lastColor):
                t.change_light(color,1)
                time.sleep(0.1)
            #print("\n\tCOLOR CHANGED:\n",color,pitch)
            
        lastColor = color
    
    lastBri = bri
    lastRms = rms
    lastPitch = pitch
    
print("* done")

print(requestsSend) #786

stream.stop_stream()
stream.close()

p.terminate()