import json
import subprocess
import glob
import os
import re
from datetime import datetime
import project_dict

# import aov_denoise as den

class rendersubmit():
    def __init__(self):
        project_dict.proj_dict().dictread()

####### BEAUTY REBUILD PLUGIN AND JOB TXT GENERATORS ########    
    def bbo_jobs(self):
        self.bbo_job_args = []
      
    def write_bbo_job(self):
        with open('args/beautyjob.txt','w') as output:
            for self.jobargs in self.bbo_job_args:
                output.write(self.jobargs + '\n')

    def bbo_plugin(self):
        self.bbo_plug_args = []

        self.exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.bbo_plug_args.append(self.exe)

        self.script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/beauty_build_oiio.py"
        self.bbo_plug_args.append(self.script)

        self.pyver = "Version=3.11"
        self.bbo_plug_args.append(self.pyver)

    def write_bbo_plug(self):
        with open('args/beautyplugin.txt','w') as output:
            for self.plugargs in self.bbo_plug_args:
                output.write(self.plugargs + '\n')

    def den_jobs(self):
        self.den_job_args = []

    def write_den_job(self):
        with open('args/denjob.txt','w') as output:
            for self.denjobargs in self.den_job_args:
                output.write(self.denjobargs + '\n')

    def den_plugin(self):
        self.den_plug_args = []

        self.den_exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.den_plug_args.append(self.den_exe)

        self.den_script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/aov_denoise.py"
        self.den_plug_args.append(self.den_script)

        self.den_plug_args.append(self.pyver)

    def write_den_plug(self):
        with open('args/denplugin.txt','w') as output:
            for self.denplugargs in self.den_plug_args:
                output.write(self.denplugargs + '\n')

    
    
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

        self.chunksize = f'ChunkSize={katargs["userchunk"]}'
        self.jobargs.append(self.chunksize)

        priority = f'Priority={katargs["userpriority"]}'
        self.jobargs.append(priority)

        pooluser = f'Pool={katargs["pool"]}'
        self.jobargs.append(pooluser)

    def writejobs(self):
        with open('args/jobs.txt','w') as output:
            for self.jobs in self.jobargs:
                output.write(self.jobs + '\n')

    # plugin file
    def pluginoptions(self,layer):
        self.plugargs = []
        # userlayer = f'RenderNode={layer}'
        # self.plugargs.append(userlayer)

    def writeplugs(self):
        with open('args/plugins.txt','w') as output:
            for self.args in self.plugargs:
                output.write(self.args + '\n')

    def write_multiple_args(self):
        with open('args/args.txt','w') as output:
            for self.line in self.args:
                output.write(self.line + '\n')

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
                framestart = project_dict.proj_dict().seqsdict[katargs["seq"]][shots]['start']
                frameend = project_dict.proj_dict().seqsdict[katargs["seq"]][shots]['end']
                
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

                    # create the variable for automated progressive steps
                    seqframes = range(int(framestart),int(frameend),1)
                    frame_len = (len(seqframes))
                    prog_step = []
                    while frame_len > 1:
                        frame_len = frame_len / 2
                        if frame_len > 1:
                            prog_step.append(int(frame_len))

                    frames_exp_list = []
                    for x in prog_step:
                        if x == 1:
                            exp = f'{framestart}-{frameend}'
                        else:
                            exp = f'{framestart}-{frameend}x{x}'
                        frames_exp_list.append(exp)
                    sep = ','
                    autoprogstep = (sep.join(frames_exp_list))
                    if frame_len == 0:
                        autoprogstep = framestart

                    fmlframes = []
                    middleframe = int((((int(frameend)) - (int(framestart)))/2)+1000)
                    fmlframes.append(framestart)
                    fmlframes.append(middleframe)
                    fmlframes.append(frameend)
                    fmlstring = ",".join(str(frm) for frm in fmlframes)
                    frames_dict = {}
                    frames_dict['Expression']= katargs['frameexp'] if katargs["stepstate"] == 0 else f'{katargs["frameexp"]}x{katargs["step"]}'
                    frames_dict['FML']= fmlstring
                    frames_dict['Keyframe'] = project_dict.proj_dict().seqsdict[katargs["seq"]][shots]['keyframe']
                    frames_dict['Shotinfo']= f'{framestart}-{frameend}' if katargs["stepstate"] == 0 else f'{framestart}-{frameend}x{katargs["step"]}'
                    frames_dict['autoprogstep'] = autoprogstep


                    # ---- writing jobs file
                    self.joboptions(katargs)
                    jobname = f'Name={katargs["seq"]}-{shots} - {layer}'
                    self.jobargs.append(jobname)
                    frames = f'Frames={frames_dict[katargs["framesdict"]]}'
                    self.jobargs.append(frames)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.lastver}/beauty'
                    self.jobargs.append(outputpathrgba)
                    outputfilergba = f'OutputFilename0={layer}_beauty.####.linear.exr'
                    self.jobargs.append(outputfilergba)
                    batchname = f'BatchName={batchnameid}'
                    self.jobargs.append(batchname)
                    katver = f'EnvironmentKeyValue0=katver={self.lastver}'
                    self.jobargs.append(katver)
                    self.writejobs()

                    # ---- writing plugin file
                    self.pluginoptions(layer)
                    layervar = f'varLayer=renderLayer={layer}'
                    self.plugargs.append(layervar)
                    shotvar = f'varShot=shot={shots}'
                    self.plugargs.append(shotvar)
                    seqvar = f'varSeq=seq={katargs["seq"]}'
                    self.plugargs.append(seqvar)
                    modevar = f'varMode=mode={katargs["mode"]}'
                    self.plugargs.append(modevar)
                    resvar = f'varRes=res={katargs["res"]}'
                    self.plugargs.append(resvar)
                    samplingvar = f'varSampling=sampling={katargs["sampling"]}'
                    self.plugargs.append(samplingvar)
                    self.writeplugs()

                    ### WRITING BEAUTY REBUILD JOBS ARGS ###
                    self.bbo_jobs()
                    self.plugin = "Plugin=Python" 
                    self.bbo_job_args.append(self.plugin)
                    comments = f'Comment={katargs["usercomment"]}'
                    self.bbo_job_args.append(comments)
                    pooluser = f'Pool={katargs["pool"]}'
                    self.bbo_job_args.append(pooluser)
                    self.name = f'Name={katargs["seq"]}-{shots} - {layer} - beauty_rebuild'
                    self.bbo_job_args.append(self.name)
                    self.user = "UserName=jonnhy"
                    self.bbo_job_args.append(self.user)
                    self.frames = frames
                    self.bbo_job_args.append(self.frames)
                    self.chunk = "ChunkSize=10" 
                    self.bbo_job_args.append(self.chunk)
                    self.bbo_job_args.append(batchname)
                    self.write_bbo_job()

                    ### WRITING BEAUTY REBUILD PLUGIN ARGS ###
                    self.bbo_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.lastver} "
                    self.arguments += "<STARTFRAME>-<ENDFRAME> "
                    self.bbo_plug_args.append(self.arguments)
                    self.bbo_plug_args.append(outputpathrgba)
                    self.bbo_plug_args.append(outputfilergba)
                    self.write_bbo_plug()

                    #### WRITING DENOISE JOB
                    self.den_jobs()
                    self.den_plug = "Plugin=Python"
                    self.den_job_args.append(self.den_plug)                    
                    
                    comments = f'Comment={katargs["usercomment"]}'
                    self.den_job_args.append(comments)

                    pooluser = f'Pool={katargs["pool"]}'
                    self.den_job_args.append(pooluser)

                    self.den_job_args.append(batchname)
                    self.den_job_name=f'Name={katargs["seq"]}-{shots} - {layer} - aov_denoise'
                    self.den_job_args.append(self.den_job_name)
                    self.den_job_args.append(self.user)
                    self.den_job_args.append(frames)
                    self.den_job_args.append(self.chunksize)
                    self.den_job_args.append(outputpathrgba)
                    self.den_job_args.append(outputfilergba)
                    self.write_den_job()

                    #### WRITING DENOISE PLUGIN
                    self.den_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.lastver} "
                    self.arguments += "<STARTFRAME>-<ENDFRAME> "
                    self.den_plug_args.append(self.arguments)
                    self.den_plug_args.append(outputpathrgba)
                    self.den_plug_args.append(outputfilergba)
                    self.write_den_plug()

                    #### WRITIG MULTIPLE JOBS ARGS
                    self.args = []

                    self.dep = "-Dependent"
                    self.job = "-Job"

                    self.submitjobs = "-SubmitMultipleJobs"
                    self.katjob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/jobs.txt'
                    self.katplug = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/plugins.txt'
                    self.katfile = f'P:/AndreJukebox/seq/{katargs["seq"]}/s0000/lighting/shot.katana'

                    self.denjob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/denjob.txt'
                    self.denplug = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/denplugin.txt'

                    self.beautyjob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/beautyjob.txt'
                    self.beautyplug = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/beautyplugin.txt'

                    self.args.append(self.submitjobs)
                    self.args.append(self.dep)
                    self.args.append(self.job)
                    self.args.append(self.katjob)
                    self.args.append(self.katplug)
                    self.args.append(self.katfile)
                    self.args.append(self.job)
                    self.args.append(self.denjob)
                    self.args.append(self.denplug)
                    self.args.append(self.job)                    
                    self.args.append(self.beautyjob)
                    self.args.append(self.beautyplug)
                    self.write_multiple_args()

                 
                    rendercommand = {
                        'Katana': f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/plugins.txt" "P:/AndreJukebox/seq/{katargs["seq"]}/s0000/lighting/shot.katana"',
                        'Nuke': f'nuke.execute({layer}, {framestart}, {frameend})'
                     }

                    command = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/plugins.txt" "P:/AndreJukebox/seq/{katargs["seq"]}/s0000/lighting/shot.katana"'
                    # subprocess.call(command, shell=True)

                    beautycommand = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/beautyjob.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/beautyplugin.txt"'
                    # subprocess.call(beautycommand, shell=True)
                    
                    denoisecommand = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/denjob.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/denplugin.txt"'
                    # subprocess.call(denoisecommand, shell=True)

                    multiplecommand = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/args.txt"'
                    subprocess.call(multiplecommand, shell=True)