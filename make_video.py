import os
import glob
import sys
import subprocess

class makeVideo:
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.version = sys.argv[3]
        self.ocio = os.getenv('ocio','')

    def make_video(self):
        source = f"P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\nuke\\latest\\temp\\{self.shot}_linear.%04d.png"
        outputfolder = f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\mov\\{self.version}'
        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)
        outputfullpath = f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\mov\\{self.version}\\{self.seq}_{self.shot}.mov'

        videocmd = f'ffmpeg -v verbose -f image2 -framerate 24 -start_number 1001 -y -i "{source}" -r 24 -c:v prores_ks -profile:v 5 -vendor apl0 -bits_per_mb 6500 -pix_fmt yuva444p10le "{outputfullpath}"'
        print(videocmd)
        subprocess.call(videocmd,shell=True)

makeVideo().make_video()