import os
import subprocess
import sys

class symlink():
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.layer = sys.argv[3]
        self.version = sys.argv[4]
        self.mode = sys.argv[5]

        print("Symlink initialized")

    def sym(self):
        layerpath = {
                    'Katana':f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\lgt\\{self.layer}\\',
                    'Nuke':f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\'
                     }
        latestpath = layerpath[self.mode] + 'latest'
        verpath = layerpath[self.mode] + self.version
        ospath = os.path.abspath(latestpath)
        print(ospath)

        if os.path.exists(ospath):
            print("LATEST exists already")
            os.remove(ospath)

        symcommand = f'mklink /D {latestpath} {verpath}'
        # net use P: \\WORKSTATION02\P /user:jonnhy Mrlikuid13! &&
        print(symcommand)
        subprocess.call(symcommand, shell=True)
symlink().sym()