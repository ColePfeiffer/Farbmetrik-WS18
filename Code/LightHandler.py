import requests
import json

def_apikey_home = "0BA43288A7"
def_ip_home = "192.168.178.37"
def_ip_digiLab = "192.168.0.180"
def_apikey_digiLab = "E44F63BE29"
def_port = "80"
def_merged = ""

location = "home"

if (location == "home"):
    def_merged = "http://"+def_ip_digiLab+":"+def_port+"/api/"+def_apikey_digiLab
else:
    def_merged = "http://"+def_ip_home+":"+def_port+"/api/"+def_apikey_home

if(False):
    url = def_merged+"/lights/1/state"
    
    data = {
        "colormode": "xy",    
        "sat": 254,
        "xy": [0.734999, 0.264986]
    }
    
    payload = json.dumps(data)
    #print(payload)
    
    try:
        r = requests.put(url, data=payload)
        print(r.status_code)
    except:
        print("There was a connection error")

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
    hue = 0
    
    url = def_merged+"/lights/1/state"
    
    if col == "blue":
        color = [0.175539, 0.026088]
    elif col == "light_blue":
        color = [0.151013, 0.134974]
    elif col == "green":
        color = [0.176305, 0.770217]
        xy = True
    elif col == "light_green":
        color = [0.335728, 0.626051]
    elif col == "red":
        color = [0.734555, 0.265062]
    elif col == "pink":
        color = [0.394583, 0.119625]
        xy = True
    elif col == "orange":
        color = [0.644679, 0.346436] #8357
        xy = True
    elif col == "yellow":
        color = [0.55491, 0.427703]
        xy = True
    elif col == "turq":
        color = [0.132631, 0.488641]
        xy = True
    elif col == "purple":
        color = [0.252225, 0.0588397]
        xy = True
    elif col == "red_pink":
        color = [0.608772, 0.211247]
    elif col == "purple_pink":
        color = [0.608772, 0.211247]   

    data = {
                "on": True,
                "colormode": "xy",
                #"hue": 1667,
                "xy": color,
                "transitiontime": tTime
        }
    
    
    payload = json.dumps(data)
    #print(payload)
    
    try:
        r = requests.put(url, data=payload)
        #print(r.status_code)
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
        #print(r.status_code)
    except:
        print("There was a connection error")

