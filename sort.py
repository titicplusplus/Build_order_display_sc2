import json
from os import listdir

data = {}

def openJson():
    global data
    with open("output.json", 'r') as json_file:
        data = json.load(json_file)

def saveJson():
    global data

    # Save the dictionary as JSON in a file
    with open("output.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("save")

openJson()

a = len(listdir("./image_final"))

for i, elem in enumerate(listdir("./image_final")):
    print(f"{i + 1}/{a}")
    print("elem :", "./image_final/" + elem)
    if elem not in data.keys():
        data[elem] = {}
        data[elem]["name"] = elem[0:-4]

        race = input("terran (t), protoss (p), zerg (z): ")
        typep = input("building (b), uints (u), upgrade (p): ")

        data[elem]["race"] = race
        data[elem]["type"] = typep

        saveJson()
