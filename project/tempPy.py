from os import listdir
from os.path import isfile, join

mypath = "./audio/"
onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)