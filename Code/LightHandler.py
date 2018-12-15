import requests
import json

def_apikey = "0BA43288A7"
def_ip = "192.168.178.37"
def_port = "80"
def_merged = "http://"+def_ip+":"+def_port+"/api/"+def_apikey

# Checks if the light is on
def isLightOn(lightNum):
    url = def_merged+"/lights/"+str(lightNum)
    r = requests.get(url)
    
    response = str(r)
    checkingFor = "\"on\": true"
           
    #checks if the string contains a certain string (substring function)
    if(response.find(checkingFor)): 
        return True
    
    return False
    
# changes the color of the light
def change_light(col, tTime):
    
    xy = False
    color = 0
    
    url = def_merged+"/lights/1/state"
    
    if col == "blue":
    	color = 47104
    elif col == "red":
        color =  60872
    elif col == "green":
        color = 25600
    elif col == "pink":
        color = 60872
    elif col == "orange":
        color = 8357
    elif col == "yellow":
        color = 7970 #12838 #7970
    elif col == "turq":
        color = 38843
    elif col == "purple":
        color = 51712
        #xy = True
            
        #data = {
         #       "on": True,
          #      "transitiontime": tTime,
          #      "xy": "[0.304432, 0.0811287]"
          #      }
        
    if(xy != True):
        data = {
                "on": True,
                "hue": color,
                "transitiontime": tTime
        }
    
    payload = json.dumps(data)
    #print(payload)
    
    try:
        r = requests.put(url, data=payload)
        print(r.status_code)
    except:
        print("There was a connection error")

# changes the brightness of the light
def change_bri(bri):   
    url = def_merged+"/lights/1/state"
    
    data = {
        "on": True,
        "bri": bri,
        #"transitiontime": 30
    }
    
    payload = json.dumps(data)
    #print(payload)
    
    try:
        r = requests.put(url, data=payload)
        print(r.status_code)
    except:
        print("There was a connection error")

