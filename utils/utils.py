import os

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