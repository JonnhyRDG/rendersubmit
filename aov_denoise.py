import os
import subprocess
import aov_dict_read
import sys

class denoise():
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.version = sys.argv[4]
        self.layer = sys.argv[3]
        self.adr = aov_dict_read.aov_dict()
        # Noise executable
        self.noice = 'P:/AndreJukebox/pipe/ktoa/KtoA4.3.3.0_kat7/bin/noice'

    def lg_denoise(self,aov,radius,frame):
        # IN AND OUT VARS
        self.lg = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/{aov}/{self.layer}_{aov}.{frame}.linear.exr'
        self.lgraw = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/{aov}/{self.layer}_{aov}_raw.{frame}.linear.exr'

        if not os.path.exists(self.lgraw):
            os.rename(self.lg,self.lgraw)
            # Beauty rename
        self.beauty = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty.{frame}.linear.exr'
        self.beautyraw = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty_raw.{frame}.linear.exr'
        
        if not os.path.exists(self.beautyraw):
            os.rename(self.beauty,self.beautyraw)

        # lg AOVS FOR DENOISING
        self.variance = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/{aov}/{self.layer}_{aov}Variance.{frame}.linear.exr'
        self.N = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/N/{self.layer}_N_denoise.{frame}.linear.exr'
        self.Z = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/depth/{self.layer}_Z_denoise.{frame}.linear.exr'
        self.albedo = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/denoise_albedo/{self.layer}_denoise_albedo.{frame}.linear.exr'
        if os.path.exists(self.beautyraw):
            while not os.path.exists(self.lg):
                self.command_lg_denoise = f'{self.noice} -pr 1 -sr {radius} -variance 0.25 -ef 2 -i {self.lgraw} -i {self.variance} -i {self.albedo} -i {self.N} -i {self.Z} -o {self.lg}'
                print(self.command_lg_denoise)
                subprocess.call(self.command_lg_denoise, shell=True)
            else:
                print(f'{aov} is already denoise at frame {frame}')

        else:
            print(f"{aov} does not exist")
            print(self.lg)

    def create_denoised(self):
        self.framerange = f'{sys.argv[5]}'
        self.adr.dictread(self.seq,self.shot,self.layer)
        for frame in range(int(self.framerange.split("-")[0]),int(self.framerange.split("-")[1])+1):
            self.aovlist = []
            for keys in self.adr.aovdict:
                self.lg_denoise(keys,self.adr.aovdict[keys],frame=frame)
                self.aovlist.append(keys)

denoise().create_denoised()