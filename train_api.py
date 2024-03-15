import requests
import json
from itertools import filterfalse

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('tfl', '2a1e95dcada140f6bed25be4718f3bb8')
out_range = False
keep_search = "y"

def Line_Status():
    line = input("\nEnter a line: ")
    if line == "pass":
        return 0

    reply = requests.get("https://api.tfl.gov.uk/Line/" + line + "/Status", auth=auth)

    data = reply.json()

    Status = (data[0]["lineStatuses"][0]["statusSeverityDescription"])

    print(Status)
    
def Station_Id():
    station = input("\nEnter a line: ")
    if station == "pass":
        return 0

    reply = requests.get("https://api.tfl.gov.uk/StopPoint/Search/" + station , auth=auth)

    data = reply.json()

    total = (data["total"])
    if total == 1:
        print("\nThere is 1 match")
    else:
        print("\nthere are ",total," matches")
    
    for i in range (total):
        if "tube" in (data["matches"][i]["modes"]):
            print(data["matches"][i]["id"] + ": " + data["matches"][i]["name"] + ", Zone: " + data["matches"][i]["zone"]) 
            print(data["matches"][i]["lat"])
            print(data["matches"][i]["lon"]) 
        else: 
            print(data["matches"][i]["id"] + ": " + data["matches"][i]["name"])
    
    retry = input("\nDo you want to search for another station id y/n?: ")
    if retry == "y":
        Station_Id()
    else:
        pass         
                        
def Lines_At_Station(out_range):
    id = input("\nEnter a station id: ")
    if id == "pass":
        return 0
    x=0
    previous_line = ""

    reply = requests.get("https://api.tfl.gov.uk/StopPoint/" + id + "/Route", auth=auth)

    data = reply.json()

    print("\nThe lines that visit this station are:\n")
    while out_range == False:
        try:
            current_line = (data[x]["lineId"])
        except IndexError:
            out_range = True
            x-=1
        if current_line != previous_line:
            print("-" + current_line)
        previous_line = current_line
        x+=1

def Line_Coordinates(): #Line coords
    line = input("\nEnter a line: ")
    if line == "pass":
        return 0

    outbound = requests.get("https://api.tfl.gov.uk/line/" + line + "/route/sequence/outbound", auth=auth)
    inbound = requests.get("https://api.tfl.gov.uk/line/" + line + "/route/sequence/inbound", auth=auth)

    out_data = outbound.json()
    in_data = inbound.json()
    
    Coordinates = []
    for i in range (len(out_data["lineStrings"])):
        x = (out_data["lineStrings"][i])
        
        x = (x.replace("[", ""))
        x = (x.replace("]", ""))
        
        x = x.split(",")
        
        x = [float(i) for i in x]
        x = [x[i:i+2] for i in range(0, len(x), 2)]
        
        Coordinates.append(x)
        
    for i in range (len(in_data["lineStrings"])):
        x = (in_data["lineStrings"][i])
        
        x = (x.replace("[", ""))
        x = (x.replace("]", ""))
        
        x = x.split(",")
        
        x = [float(i) for i in x]
        x = [x[i:i+2] for i in range(0, len(x), 2)]
        
        Coordinates.append(x)
    
    if len(out_data["lineStrings"]) > 1:
        longest = (max(Coordinates, key=len))
        x=0
        for i in range (len(out_data["lineStrings"])+len(in_data["lineStrings"])):
            if (Coordinates[i-x][-1]) != (longest[-1]) and (Coordinates[i-x][-1]) != (longest[0]):
                Coordinates.remove(Coordinates[i-x])
                x+=1
        
        x=0
        for i in range (len(Coordinates)-1):
            remove = list(filterfalse(longest.__contains__,Coordinates[i+1]))
            Coordinates[i+1]=(remove)
            
    elif len(out_data["lineStrings"]) == 1:
        del Coordinates[-1]
                
    Coordinates = list(filter(None, Coordinates))
    for i in range (len(Coordinates)):
        print ("Branch",i,Coordinates[i],len(Coordinates[i]),":\n\n")
    
def Search():
    search = input("\nChoose a search\n1: Line status\n2: Station id\n3: Lines at station\n4: Line coordinates\n")
    if search == "1":
        Line_Status()
    elif search == "2":
        Station_Id()
    elif search == "3":
        Lines_At_Station(out_range)
    elif search == "4":
        Line_Coordinates()
    else:
        print("ERROR: invalid number")
    
while keep_search == "y":
    Search()
    keep_search = input("\nDo you wish to keep searching y/n?: ")
print("-------------Search ended-------------")