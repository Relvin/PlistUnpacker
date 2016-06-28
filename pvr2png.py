#encoding=utf8

import os
import sys
SUFFIX = ".pvr.ccz"

def GetTexturePackerPath():
	if(os.name == 'posix'):
		return '/usr/local/bin/TexturePacker '
	else:
		return 'TexturePacker.exe '

def pvrToPng (_path,_OutPath):
    OutPath = _OutPath
    for(dirpath, dirnames, filenames) in os.walk(_path):
        for filename in filenames:
            if filename.endswith(SUFFIX):
                basename = os.path.basename(filename)
                newFileName = basename[0:basename.find(SUFFIX)]
                if not os.path.isabs(_OutPath):
                    OutPath = os.path.join(dirpath,_OutPath)
                # deltaPath = dirpath
                if not os.path.exists(OutPath):
                    os.makedirs(OutPath)
                outFileName = os.path.join(OutPath,newFileName + ".png")
                cmd = GetTexturePackerPath() + os.path.join(dirpath,filename) + " --data pvr2png.plist "  + " --sheet " + outFileName + " --opt RGBA8888"
                os.system(cmd)
    os.remove("pvr2png.plist")
    print "pvrToPng"

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("usage : python pvr2png.py [source Path] [suffix] [OutPath:option]")
    else:
        SUFFIX = sys.argv[2]
        OutPath = './'
        if len(sys.argv) == 4:
            OutPath = sys.argv[3]
        if SUFFIX[0] != '.':
            SUFFIX = "." + SUFFIX
        pvrToPng(sys.argv[1],OutPath)