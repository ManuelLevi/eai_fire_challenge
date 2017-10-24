from sys import exit
import json
import os
import pandas


data = []
for root, dirs, files in os.walk("DATA"):
    for file in files:
        if file == 'tileInfo.json':
            filename = os.path.join(root, file)
            with open(filename, 'r') as json_file:
                data.append(json.load(json_file))


data = pandas.DataFrame(data)

print(data)