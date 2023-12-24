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

for race in ["Terran", "Protoss", "Zerg"]:
    print(f"class {race}:")
    firstletter = race[0].lower()
    print("\tclass Structure:")
    print(render[firstletter + "b"])
    print("\tclass Units:")
    print(render[firstletter + "u"])
    print("\tclass Upgrade:")
    print(render[firstletter + "u"])

