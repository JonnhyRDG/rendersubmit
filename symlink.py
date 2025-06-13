import os
import subprocess
import sys

class symlink():
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.version = sys.argv[4]
        self.layer = sys.argv[3]

        print("Symlink initialized")

    def sym(self):
        layerpath = f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\lgt\\{self.layer}\\'
        latestpath = layerpath + 'latest'
        verpath = layerpath + self.version
        print(latestpath)
        if os.path.exists(os.path.abspath(latestpath)):
            
            print("LATEST exists already")
            delcommand = f'rmdir {latestpath}'
            subprocess.call(delcommand, shell=True)
            os.remove(latestpath)

        symcommand = f'mklink /D {latestpath} {verpath}'
        # net use P: \\WORKSTATION02\P /user:jonnhy Mrlikuid13! &&
        print(symcommand)
        subprocess.call(symcommand, shell=True)
symlink().sym()