from shutil import copyfile
import os

profileList = os.listdir(path="C:\\Users\\mo.battah\\Documents\\WebLog\\Profiles")  #Fill in where your profiles are located
url = "C:\\Users\\mo.battah\\Documents\\WebLog\\Profiles"
url2 = "C:\\Users\\mo.battah\\Documents\\WebLog\\Profiles\\" #url2 keeps the last two slashes
#print(profileList)

for item in profileList:
    fname = item[0:len(item)-4] #getting the filename without extension
    if fname.isdigit() == True: #comparing that to an integer to see if needs be copied/renamed
        fp = open(url2+item, 'r') #opens pfl file and reads
        line = fp.readlines()
        print(line[1])
        line = line[1] #Gets the Name= line
        profileName = str(line[5:len(line) - 1])
        print(profileName)
        namesource = url2 + fname + ".pfl"
        print(namesource)
        namedest = profileName + ".pf1"
        namedest = namedest.replace('\\','_')
        namedest = namedest.replace('/','_')
        namedest = namedest.replace('*','_')
        namedest = url2 + namedest
        print(namesource)
        print(namedest)
        try: copyfile(namesource, namedest)
        except FileNotFoundError:
            print("This will need a check: " + namedest)
    else:
        print("Please check " + item)
