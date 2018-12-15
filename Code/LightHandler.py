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
    pink = 60872
    #red = "\"xy\": [0.73097, 0.263515],"
    green = 25600
    blue = 47104
    yellow = 12838
    orange = 8357
    red = 60872
    #pink1 = 59695

    color = 0
    url = def_merged+"/lights/1/state"
    
    if col == "blue":
    	color = blue
    elif col == "red":
        color = red
    elif col == "green":
        color = green
    elif col == "pink":
        color = pink
    elif col == "orange":
        color = orange
    elif col == "yellow":
        color = yellow
        
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

