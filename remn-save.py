import binascii
import os
import shutil
from os import path

userID = "USERIDFOLDER"

base = path.expandvars(r'%localappdata%')
folder = base +  "/Packages/PerfectWorldEntertainment.GFREMP2_jrajkyc4tsa6w/SystemAppData/wgs/" +userID + "/"
containers = folder + 'containers.index'

profileidx = 329
offset = 119

#save_0idx = 448
#save_1idx = 567
#save_2idx = 686
idxorder = [3,2,1,0,5,4,7,6,8,9,10,11,12,13,14,15]
profilefolder = ''
profilefile=''

savefolder = ''
savefilename = []
savefilenames = []

containeridx = 136
containersize = 0

def getsavefiles(file_number) :
    if containersize > profileidx+(offset*(file_number))+16  :
        with open(containers, 'rb') as idx:
            string = b''
            for i in idxorder:
                idx.seek(profileidx+offset*(file_number)+i)
                string += binascii.b2a_hex(idx.read(1))
            savefolder = folder + string.decode('ascii').upper()
        file_list = os.listdir(savefolder)
        container_list = [file for file in file_list if file.startswith('container.')]
        with open(savefolder + "/" + container_list[0],'rb') as idx:
            string = b''
            for i in idxorder:
                idx.seek(containeridx+i)
                string += binascii.b2a_hex(idx.read(1))
            savefilenames.append(savefolder + '/' + string.decode('ascii').upper())
            if file_number == 0 :
                savefilename.append('profile.sav')
            else:
                savefilename.append('save_'+str(file_number-1)+'.sav')
    else :
        exit

if len(userID) < 40:
    print('set userID in remn-save.py')
    exit(1)
    
if path.exists(containers):
    containersize = os.path.getsize(containers)
    if containersize < (profileidx + offset + 16):
        print('containers.index is too short')
        exit(1)
    else:
        currentoffset = 0
        fn=0
        while containersize > currentoffset:
            getsavefiles(fn)
            currentoffset = profileidx + (offset*(fn+1))
            fn=fn+1
        if len(savefilename) == len(savefilenames) :
            for i in range(0,len(savefilename)):
                print(savefilename[i],"\n",savefilenames[i])
                shutil.copy(savefilenames[i],savefilename[i])
else :
    print('containers.index not found')
    exit(1)
