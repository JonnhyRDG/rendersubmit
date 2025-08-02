import os
import aov_dict_read
import sys
import glob

class aov_rename():
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.layer = sys.argv[3]
        self.version = sys.argv[4]
        self.adr = aov_dict_read.aov_dict()

        # Noise executable
        self.noice = 'P:/AndreJukebox/pipe/ktoa/KtoA4.3.3.0_kat7/bin/noice'

    def prep_aov(self):
        self.adr.dictread(self.seq,self.shot,self.layer)
        for aov in self.adr.aovdict:
            self.aov = f'P:\\AndreJukebox_output\\renders\\concept_animatic\\{self.seq}\\{self.shot}\\lgt\\{self.layer}\\{self.version}\\{aov}\\'
            search_files = glob.glob(f'{self.aov}*')
            for aov_file in search_files:
                if f'_{aov}.' in aov_file and not f'_{aov}_raw.' in aov_file:
                    aov_rename = aov_file.replace(f'_{aov}.',f'_{aov}_raw.')
                    if not os.path.exists(aov_rename):
                        os.rename(aov_file,aov_rename)
                        print("Rename done")
                else:
                    print("Either Variance file found or _raw aov already done.")

aov_rename().prep_aov()