import OpenImageIO as oiio
import os
import sys
import aov_dict_read
# import symlink as sl

class beautyBuild:
    def __init__(self):
        self.seq = sys.argv[1]
        self.shot = sys.argv[2]
        self.version = sys.argv[4]
        self.layer = sys.argv[3]
        self.adr = aov_dict_read.aov_dict()
        self.subs_combined_buf = None
        self.subs_combined_buf_den = None

    def clear_buffer(self):
        self.subs_combined_buf = None
        self.subs_combined_buf_den = None        
    
    def beauty_paths(self,frame):
        # path for the final denoised beauty
        self.beauty = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty.{frame}.linear.exr'

        # path for the raw beauty
        self.beautyraw = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty_raw.{frame}.linear.exr'

        # this is where we will write to disk the sum of all aovs we want to substract from beauty.
        self.beautysub = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty_sub.{frame}.linear.exr'

    def buffer_beauty(self):
        # this starsts the buffer for the beauty, this is the raw version, no denoise, no nothing.
        self.beautyraw_buf = oiio.ImageBuf(self.beautyraw)

        # Initializing the buffer for the raw beauty
        self.result = oiio.ImageBuf(self.beautyraw_buf.spec())
        
        #This is the final path of the beauty denoised
        self.output = self.beauty

        # this is a temporary path, of the beauty with the substractions
        self.outputsub = self.beautysub

    def add_lg_subs(self,aov,frame):
        # form the path of the aov. "lgraw" stands for light group raw, so not the denoised one.
        self.lgraw = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/{aov}/{self.layer}_{aov}_raw.{frame}.linear.exr'
        
        # create the buffer for the aov
        self.subs_buf = oiio.ImageBuf(self.lgraw)

        # generate a path, for the output adding up all of the aovs. This is what we will substract from the beauty later.
        self.lgaddsubs = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty_addsubs.{frame}.linear.exr'

        # so we're going to check that the combined aovs i None to beggin with. That will be true only the first time, so it will trigger the generation of a temporary buffer.
        if self.subs_combined_buf is None:
            # this is the initialization of the aov buffer, the raw un denoised aov.
            self.subs_combined_buf = oiio.ImageBuf(self.subs_buf.spec())

            # we'll copy the content of that raw aov into the combined one, which was empty so far, in the first iteration of the loop.
            oiio.ImageBufAlgo.copy(self.subs_combined_buf,self.subs_buf)
        else:
            # we'll create another buffer, a temp one with the combined buffer content and initialize it.
            self.subs_temp_buf = oiio.ImageBuf(self.subs_combined_buf.spec())

            # add up the raw aovs
            oiio.ImageBufAlgo.add(self.subs_temp_buf,self.subs_combined_buf,self.subs_buf)

            # copy the content of the combined buffer into the temporary one
            oiio.ImageBufAlgo.copy(self.subs_combined_buf, self.subs_temp_buf)

        
        self.subs_combined_buf.write(self.lgaddsubs)

    def add_lg_adds(self,aov,frame):
        # all of these steps are the same as above, except now we're using the denoised aovs, and generating a combined denoised image.
        self.lg = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/{aov}/{self.layer}_{aov}.{frame}.linear.exr'
        self.subs_buf_den = oiio.ImageBuf(self.lg)
        self.lgaddadds = f'P:/AndreJukebox_output/renders/concept_animatic/{self.seq}/{self.shot}/lgt/{self.layer}/{self.version}/beauty/{self.layer}_beauty_addadds.{frame}.linear.exr'

        if self.subs_combined_buf_den is None:
            self.subs_combined_buf_den = oiio.ImageBuf(self.subs_buf_den.spec())
            oiio.ImageBufAlgo.copy(self.subs_combined_buf_den,self.subs_buf_den)
        else:
            self.subs_temp_buf_den = oiio.ImageBuf(self.subs_combined_buf_den.spec())
            oiio.ImageBufAlgo.add(self.subs_temp_buf_den,self.subs_combined_buf_den,self.subs_buf_den)
            oiio.ImageBufAlgo.copy(self.subs_combined_buf_den, self.subs_temp_buf_den)
        self.subs_combined_buf_den.write(self.lgaddadds)

    def substract_lgs(self):
        # create the 
        self.lgaddsubs_buf = oiio.ImageBuf(self.lgaddsubs)

        # this is the actual substraction operation
        oiio.ImageBufAlgo.sub(self.result, self.beautyraw_buf, self.lgaddsubs_buf)

        # and now we're writing our buffer out
        self.result.write(self.outputsub)


    def add_lgs(self):
        # buffer to add to beauty
        self.lgaddadds_buf = oiio.ImageBuf(self.lgaddadds)
        
        # buffer of the output we'll write on disk.
        self.subbuf = oiio.ImageBuf(self.outputsub)
        
        # this is the actual substraction operation
        oiio.ImageBufAlgo.add(self.result, self.subbuf, self.lgaddadds_buf)

        # and now we're writing our buffer out
        self.result.write(self.output)

    # we'll generate a bunch of temp files on disk, which is the combined raw aovs, combined denoised aovs and a beauty with substracted lights.
    # And after they have been used in the buffers to operate, we'll get rid of them.
    def clean_up(self):
        # add in pathlist all the paths you want to get rid of.
        pathlist = [self.lgaddadds,self.lgaddsubs,self.outputsub]

        # checking if the paths exist, and in that case, nuke'em. 
        for file in pathlist:
            if os.path.exists(file):
                os.remove(file)

    def frames_range(self):
        self.framerange = f'{sys.argv[5]}'
        # self.framerange = '1001-1002'

    def rebuild_beauty(self):
        # the dictionary below is a list of aov and a digit pair, the digit is the level of denoise.
        # it will generated through a tool from nuke, where I review each aov to be denoised.
        # This way we avoid smoothing the whole image out, picking and choosing what to denoise
        # AND being a bit more efficient resources wise.
        self.adr.dictread(self.seq,self.shot,self.layer)
        self.frames_range()

        # checking if the shot dictionary exists
        if os.path.exists(self.adr.jsonpath):
            self.frames_range()
            # wrap the beautyBuild class in a var because I'm lazy
            for frame in range(int(self.framerange.split("-")[0]),int(self.framerange.split("-")[1])+1):
                self.clear_buffer()
                self.beauty_paths(frame)
                self.buffer_beauty()
                # This will loop through the dict and operate with each key to output the auxiliary exrs
                for key in self.adr.aovdict:
                        self.add_lg_subs(key,frame)
                        self.add_lg_adds(key,frame)
                # in this step it will substract the combined aovs from beauty
                self.substract_lgs()

                # Add up the denoised aovs to the substracted beauty.
                self.add_lgs()

                # Get rid of the auxiliary files.
                self.clean_up()
        # sl.symlink().sym(seq=self.seq,shot=self.shot,layer=self.layer,version=self.version)

bbo = beautyBuild()
bbo.rebuild_beauty()