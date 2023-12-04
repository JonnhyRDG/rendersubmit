import json
import subprocess
import glob
import os
import re
from datetime import datetime
import project_dict

class rendersubmit():
    def __init__(self):
        project_dict.dictread(self)

    # jobs file
    def joboptions(self,katargs):
        # add arguments to jobargs list
        self.jobargs = []

        # arguments and adding to list
        plugin = f'Plugin={katargs["userdcc"]}'
        self.jobargs.append(plugin)

        comments = f'Comment={katargs["usercomment"]}'
        self.jobargs.append(comments)

        initialstatus = f'InitialStatus={katargs["userstatus"]}'
        self.jobargs.append(initialstatus)

        chunksize = f'ChunkSize={katargs["userchunk"]}'
        self.jobargs.append(chunksize)

        priority = f'Priority={katargs["userpriority"]}'
        self.jobargs.append(priority)

        pooluser = f'Pool={katargs["pool"]}'
        self.jobargs.append(pooluser)

    def writejobs(self):
        with open('jobs.txt','w') as output:
            for self.jobs in self.jobargs:
                output.write(self.jobs + '\n')

    # plugin file
    def pluginoptions(self,layer):
        self.plugargs = []
        # userlayer = f'RenderNode={layer}'
        # self.plugargs.append(userlayer)

    def writeplugs(self):
        with open('plugins.txt','w') as output:
            for self.args in self.plugargs:
                output.write(self.args + '\n')

    # cmds file
    def cmdsoptions(self):
        self.cmdsargs = []

    def writecmds(self):
        with open('commands.txt','w') as output:
            output.write('/n'.join(self.cmdsargs))            

    def submit(self,katargs):
        for shotdict in katargs['shotsdict']:
            for shots in shotdict:
                batchnameid = f'{katargs["seq"]}-{shots}__[{datetime.now().strftime("%d%m%Y%H%M%S")}]'
                framestart = self.seqsdict[katargs["seq"]][shots]['start']
                frameend = self.seqsdict[katargs["seq"]][shots]['end']
                
                for layer in shotdict[shots]:
                    # getting the version #
                    self.path = f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/*'
                    self.verfolder = glob.glob(self.path)
                    self.verlist = []
                    for self.ver in self.verfolder:
                        self.verpath = os.path.abspath(self.ver)
                        self.verfolder = self.verpath.rsplit('\\',1)[1]
                        if re.match('\d{4}',self.verfolder):
                            self.verlist.append(self.verfolder)
                    if not self.verlist:
                        self.verlist.append('0001')
                        self.lastver = '0001'
                    else:
                        if katargs['version'] == 1:
                            self.lastver = str(f'{int(self.verlist[-1]) + 1:04d}')

                        else:
                            self.lastver = str(f'{int(self.verlist[-1]):04d}')
                    createdir = f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.lastver}'
                    if not os.path.isdir(createdir):
                        os.makedirs(createdir)                    

                    fmlframes = []
                    middleframe = int((((int(frameend)) - (int(framestart)))/2)+1000)
                    fmlframes.append(framestart)
                    fmlframes.append(middleframe)
                    fmlframes.append(frameend)
                    fmlstring = ",".join(str(frm) for frm in fmlframes)
                    frames_dict = {}
                    frames_dict['Expression']= katargs['frameexp'] if katargs["stepstate"] == 0 else f'{katargs["frameexp"]}x{katargs["step"]}'
                    frames_dict['FML']= fmlstring 
                    frames_dict['Shotinfo']= f'{framestart}-{frameend}' if katargs["stepstate"] == 0 else f'{framestart}-{frameend}x{katargs["step"]}'

                    # ---- writing jobs file
                    self.joboptions(katargs)
                    jobname = f'Name={katargs["seq"]}-{shots} - {layer}'
                    self.jobargs.append(jobname)
                    frames = f'Frames={frames_dict[katargs["framesdict"]]}'
                    self.jobargs.append(frames)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.lastver}/rgba'
                    self.jobargs.append(outputpathrgba)
                    outputfilergba = f'OutputFilename0={layer}_rgba.####.linear.exr'
                    self.jobargs.append(outputfilergba)
                    batchname = f'BatchName={batchnameid}'
                    self.jobargs.append(batchname)
                    katver = f'EnvironmentKeyValue0=katver={self.lastver}'
                    self.jobargs.append(katver)
                    # self.postscript = f'PreJobScript=p:/AndreJukebox/pipe/ajbackend/rendersubmit/rendersubmit_ui.py'
                    # self.jobargs.append(self.postscript)
                    self.writejobs()

                    # ---- writing plugin file
                    self.pluginoptions(layer)
                    layervar = f'varLayer=renderLayer={layer}'
                    self.plugargs.append(layervar)
                    shotvar = f'varShot=shot={shots}'
                    self.plugargs.append(shotvar)
                    seqvar = f'varSeq=seq={katargs["seq"]}'
                    self.plugargs.append(seqvar)
                    self.writeplugs()
                    
                    rendercommand = {
                        'Katana': f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/plugins.txt" "P:/AndreJukebox/seq/{katargs["seq"]}/s0000/lighting/shot.katana"',
                        'Nuke': f'nuke.execute({layer}, {framestart}, {frameend})'
                     }
                    print(rendercommand[katargs['userdcc']])
                    command = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/plugins.txt" "P:/AndreJukebox/seq/{katargs["seq"]}/s0000/lighting/shot.katana"'
                    subprocess.call(command, shell=True)