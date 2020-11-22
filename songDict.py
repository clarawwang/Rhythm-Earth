import json
import os.path
from os import path

json_data = '{"name": "Brian", "city": "Seattle"}'
python_obj = json.loads(json_data)
print(python_obj["name"])
print(python_obj["city"])

def songDict(tup):
    if os.path.exists("songsDict.txt"):
        diff = str(tup[1])
        newKey = tup[0] + diff
        with open("songsDict.txt") as json_data:
            dictPy = json.load(json_data)
            return dictPy[newKey]
    else:
        diff = str(tup[1])
        newKey = tup[0] + diff
        dict1 = {newKey:{1:2}}
        with open("songsDict.txt", 'w') as outfile:
            json.dump(dict1, outfile)
        return json.loads(dict1[newKey])

print(songDict(("people", 2)))