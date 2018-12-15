import LightHandler as liH
import time

def run():
    while (True):
        liH.change_light(1)
        time.sleep(10)
        # Erst State vom Server Holen
        # Dann Hue anpassen

if __name__ == "__main__":
    
    print(liH.isLightOn(1))
        
    i = 1    
    while(i <= 3):
        liH.change_light(i)
        time.sleep(5)
        i = i+1
    #run()

