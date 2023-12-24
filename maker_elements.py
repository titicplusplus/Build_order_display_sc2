import json

data = {}

def openJson():
    global data
    with open("output.json", 'r') as json_file:
        data = json.load(json_file)

render = {"tb": "", "tu": "", "tp": "", "pb": "", "pu": "", "pp": "", "zb": "", "zu": "", "zp": ""}

openJson()

for key, value in data.items():
    place = value["race"] + value["type"]
    render[place] += "\t\t" + value["name"] + "\t\t\t= '" + key + "'\n"

data = ""

for race in ["Terran", "Protoss", "Zerg"]:
    data += f"class {race}:\n"
    firstletter = race[0].lower()
    data += "\tclass Structure:\n"
    data += render[firstletter + "b"] + "\n"
    data += "\tclass Units:\n"
    data += render[firstletter + "u"] + "\n"
    data += "\tclass Upgrade:\n"
    data += render[firstletter + "p"] + "\n"

print(data)

with open("./sc2_elements.py", "w") as f:
    f.write(data)

