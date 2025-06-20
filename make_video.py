import os
import glob
import sys
import subprocess

class makeVideo:
    def __init__(self):
            
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        # self.seq = '010_NCT'
        # self.shot = 's0100'
        self.exrversion = glob.glob(f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\latest\\raw\\*")
        self.ocio = os.getenv('ocio','')
        self.exr = []
        self.png = []

    def make_png(self):
        for self.exr in self.exrversion:
            self.tempdir = f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\latest\\temp\\"
            self.png = (self.exr.replace('exr','png').replace("raw","temp"))
            self.exrcolor = 'linear'
            self.transformcolor = 'BT.1886 Filmic Log Encoding High Contrast'
            self.pngcmd = f'oiiotool "{self.exr}" --colorconfig {self.ocio} --colorconvert "{self.exrcolor}" "{self.transformcolor}" -o {self.png}'
            if not os.path.exists(self.tempdir):
                os.mkdir(self.tempdir)
            subprocess.call(self.pngcmd,shell=True)
        self.make_video()

    def make_video(self):
        print(self.png)
        replace = self.png.rsplit('.',2)[1]
        source = self.png.replace(replace,'%04d')
        output = f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\mov\\latest\\{self.seq}_{self.shot}.mov'

        videocmd = f'ffmpeg -f image2 -start_number 1001 -y -i "{source}" -r 24 -c:v prores_ks -profile:v 3 -vendor apl0 -bits_per_mb 6500 -pix_fmt yuv422p10le "{output}"'
        print(videocmd)
        subprocess.call(videocmd,shell=True)

makeVideo().make_png()