import os
import glob
import sys
import subprocess

class makeVideo:
    def __init__(self):
            
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.version = sys.argv[3]
        self.framerange = sys.argv[4]
        self.exrversion = f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\{self.version}\\raw\\{self.shot}"
        self.ocio = os.getenv('ocio','')
        self.exr = []
        self.png = []

    def make_convert(self):
        for frame in range(int(self.framerange.split("-")[0]),int(self.framerange.split("-")[1])+1):
            self.exrversion = f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\{self.version}\\raw\\{self.shot}_linear.{frame}.exr"
            self.tempdir = f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\{self.version}\\temp\\"
            self.png = (self.exrversion.replace('exr','png').replace("raw","temp"))
            self.exrcolor = 'linear'
            self.transformcolor = 'BT.1886 Filmic Log Encoding High Contrast'
            self.pngcmd = f'oiiotool "{self.exrversion}" --colorconfig {self.ocio} --colorconvert "{self.exrcolor}" "{self.transformcolor}" -o {self.png}'
            if not os.path.exists(self.tempdir):
                os.mkdir(self.tempdir)
            subprocess.call(self.pngcmd,shell=True)
            print(f'{frame} converted.')


makeVideo().make_convert()