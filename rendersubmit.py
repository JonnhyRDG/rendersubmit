import json
import subprocess
from datetime import datetime
class rendersubmit():
    def __init__(self):
        self.dictread()

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)

    # jobs file
    def joboptions(self,seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk,framesdict,pool):
        # add arguments to jobargs list
        self.jobargs = []

        # arguments and adding to list
        plugin = f'Plugin={userdcc}'
        self.jobargs.append(plugin)

        comments = f'Comment={usercomment}'
        self.jobargs.append(comments)

        initialstatus = f'InitialStatus={userstatus}'
        self.jobargs.append(initialstatus)

        chunksize = f'ChunkSize={userchunk}'
        self.jobargs.append(chunksize)

        priority = f'Priority={userpriority}'
        self.jobargs.append(priority)

        pooluser = f'Pool={pool}'
        self.jobargs.append(pooluser)

    def writejobs(self):
        with open('jobs.txt','w') as output:
            output.write('\n'.join(self.jobargs))

    # plugin file
    def pluginoptions(self,layer):
        self.plugargs = []
        # userlayer = f'RenderNode={layer}'
        # self.plugargs.append(userlayer)

    def writeplugs(self):
        with open('plugins.txt','w') as output:
            output.write('\n'.join(self.plugargs))

    # cmds file
    def cmdsoptions(self):
        self.cmdsargs = []

    def writecmds(self):
        with open('commands.txt','w') as output:
            output.write('\n'.join(self.cmdsargs))            

    def submit(self,seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk,framesdict,frameexp,step,stepstate,pool):
        for shots in shotsdict:
            batchnameid = f'{seq}-{shots}__[{datetime.now().strftime("%d%m%Y%H%M%S")}]'
            framestart = self.seqsdict[seq][shots]['start']
            frameend = self.seqsdict[seq][shots]['end']
            for layer in shotsdict[shots]:
                fmlframes = []
                middleframe = int((((int(frameend)) - (int(framestart)))/2)+1000)
                fmlframes.append(framestart)
                fmlframes.append(middleframe)
                fmlframes.append(frameend)
                fmlstring = ",".join(str(frm) for frm in fmlframes)
                frames_dict = {}
                frames_dict['Expression']= frameexp if stepstate == 0 else f'{frameexp}x{step}'
                frames_dict['FML']= fmlstring 
                frames_dict['Shotinfo']= f'{framestart}-{frameend}' if stepstate == 0 else f'{framestart}-{frameend}x{step}'

                # ---- writing jobs file
                self.joboptions(seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk,framesdict,pool)
                
                jobname = f'Name={seq}-{shots} - {layer}'
                self.jobargs.append(jobname)
                
                frames = f'Frames={frames_dict[framesdict]}'
                self.jobargs.append(frames)
                
                outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{seq}/{shots}/lgt/{layer}/latest/rgba'
                self.jobargs.append(outputpathrgba)
                
                outputfilergba = f'OutputFilename0={layer}_rgba.####.linear.exr'
                self.jobargs.append(outputfilergba)

                batchname = f'BatchName={batchnameid}'
                self.jobargs.append(batchname)
                self.writejobs()

                # ---- writing plugin file
                self.pluginoptions(layer)
                layervar = f'varLayer=renderLayer={layer}'
                self.plugargs.append(layervar)
                shotvar = f'varShot=shot={shots}'
                self.plugargs.append(shotvar)
                seqvar = f'varSeq=seq={seq}'
                self.plugargs.append(seqvar)
                self.writeplugs()

                command = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/plugins.txt" "P:/AndreJukebox/seq/{seq}/s0000/lighting/shot.katana"'
                subprocess.call(command, shell=True)