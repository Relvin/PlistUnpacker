#encoding=utf8

import os
import sys
SUFFIX = ".pvr.ccz"

def curl_taobao ():
    # curl_init()
    print("")
def GetTexturePackerPath():
	if(os.name == 'posix'):
		return '/usr/local/bin/TexturePacker '
	else:
		return 'TexturePacker.exe '

def pvrToPng (_path,OutPath):

    index = 0
    for(dirpath, dirnames, filenames) in os.walk(_path):
        for filename in filenames:
            if filename.endswith(SUFFIX):
                newFileName = filename[0:filename.find(SUFFIX)]

                if not os.path.exists(os.path.join(_path,OutPath)):
                    os.makedirs(os.path.join(_path,OutPath))
                cmd = GetTexturePackerPath() + os.path.join(dirpath,filename) + " --sheet " +  _path + OutPath + newFileName + ".png" + " --opt RGBA8888 --allow-free-size --algorithm Basic --no-trim --dither-fs"
                os.system(cmd)

    print "pvrToPng"

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("usage : python pvr2png.py [Directory] [suffix] [OutPath:option]")
    else:
        SUFFIX = sys.argv[2]
        OutPath = './'
        if len(sys.argv) == 4:
            OutPath = sys.argv[3]
        if SUFFIX[0] != '.':
            SUFFIX = "." + SUFFIX
        pvrToPng(sys.argv[1],OutPath)