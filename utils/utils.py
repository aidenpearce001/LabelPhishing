import os
import pandas as pd

def readTxt(path):
    with open(path) as f:
        urls = f.readlines()
    urls = ([s.strip('\n') for s in urls ])
    return urls 

def labelFolder(directory):
    path = os.path.join(os.getcwd(), directory) 
    isExist = os.path.exists(path) 
    if isExist:
        pass
    else:
        os.mkdir(path)

def toCSV(path, data):
    json = []
    json.append(list(data.values()))
    df = pd.DataFrame(json)
    df.to_csv(f'{path}/label.csv', mode='a', header = False)