import subprocess
import glob
import os
import re
import project_dict
import aov_dict_read 

class rendersubmit():
    def __init__(self):
        project_dict.proj_dict().dictread()
        self.adr = aov_dict_read.aov_dict()

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

    def rename_jobs(self):
            self.rename_job_args = []

    def write_rename_job(self):
        with open('args/renamejob.txt','w') as output:
            for self.renamejobargs in self.rename_job_args:
                output.write(self.renamejobargs + '\n')

    def rename_plugin(self):
        self.rename_plug_args = []

        self.rename_exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.rename_plug_args.append(self.rename_exe)

        self.rename_script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/aov_rename.py"
        self.rename_plug_args.append(self.rename_script)

        self.rename_plug_args.append(self.pyver)

    def write_rename_plug(self):
        with open('args/renameplugin.txt','w') as output:
            for self.renameplugargs in self.rename_plug_args:
                output.write(self.renameplugargs + '\n')

    def sym_jobs(self):
        self.sym_job_args = []

    def write_sym_job(self):
        with open('args/symjob.txt','w') as output:
            for self.symjobargs in self.sym_job_args:
                output.write(self.symjobargs + '\n')

    def write_symnuke_job(self):
        with open('args/symnukejob.txt','w',encoding="utf-8") as output:
            for self.symnukejobargs in self.sym_job_args:
                output.write(self.symnukejobargs + '\n')

    def sym_plugin(self,dcc):
        self.sym_plug_args = []

        self.sym_exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.sym_plug_args.append(self.sym_exe)

        self.sym_script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/symlink.py"
        self.sym_plug_args.append(self.sym_script)

        self.sym_plug_args.append(self.pyver)
        
        self.dcc = f"{dcc} "

    def write_symnuke_plug(self):
        with open('args/symnukeplugin.txt','w') as output:
            for self.symnukeplugargs in self.sym_plug_args:
                output.write(self.symnukeplugargs + '\n')

    def write_sym_plug(self):
            with open('args/symplugin.txt','w') as output:
                for self.symplugargs in self.sym_plug_args:
                    output.write(self.symplugargs + '\n')
    def write_symvideo_job(self):
        with open('args/symvideojob.txt','w',encoding="utf-8") as output:
            for self.symvideojobargs in self.sym_job_args:
                output.write(self.symvideojobargs + '\n')

    def write_symvideo_plug(self):
        with open('args/symvideoplugin.txt','w') as output:
            for self.symvideoplugargs in self.sym_plug_args:
                output.write(self.symvideoplugargs + '\n')

    def nuke_jobs(self):
        self.nuke_job_args = [
        'Blacklist=',
        'ChunkSize=10',
        'EventOptIns=',
        'OverrideTaskExtraInfoNames=False',
        'Plugin=Nuke',
        'Region=',
        'UserName=jonnhy'
        ]

    def write_nuke_job(self):
        with open('args/nukejob.txt','w',encoding="utf-8") as output:
            for self.nukejobargs in self.nuke_job_args:
                output.write(self.nukejobargs + '\n')

    def nuke_plugin(self):
        self.nuke_plugin_args = ['BatchMode=True',
                               'BatchModeIsMovie=False',
                               'ContinueOnError=False',
                               'EnforceRenderOrder=False',
                               'GpuOverride=0',
                               'NukeX=False',
                               'PerformanceProfiler=False',
                               'RamUse=0',
                               'RenderMode=Render Full Resolution',
                               'StackSize=0',
                               'Threads=0',
                               'UseGpu=False',
                               'UseSpecificGpu=False',
                               'Version=15.0',
                               'Views=']
        
    def write_nuke_plugin(self):
        with open('args/nukeplugin.txt','w') as output:
            for self.nukepluginargs in self.nuke_plugin_args:
                output.write(self.nukepluginargs + '\n')

    def video_jobs(self):
        self.video_job_args = []
        
    def write_video_job(self):
        with open('args/videojob.txt','w') as output:
            for self.jobargs in self.video_job_args:
                output.write(self.jobargs + '\n')

    def video_plugin(self):
        self.video_plug_args = []

        self.exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.video_plug_args.append(self.exe)

        self.script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/make_video.py"
        self.video_plug_args.append(self.script)

        self.pyver = "Version=3.11"
        self.video_plug_args.append(self.pyver)

    def write_video_plug(self):
        with open('args/videoplugin.txt','w') as output:
            for self.jobargs in self.video_plug_args:
                output.write(self.jobargs + '\n')

    def convert_jobs(self):
        self.convert_job_args = []
        
    def write_convert_job(self):
        with open('args/convertjob.txt','w') as output:
            for self.jobargs in self.convert_job_args:
                output.write(self.jobargs + '\n')

    def convert_plugin(self):
        self.convert_plug_args = []

        self.exe = "Executable=C:/Program Files/Python311/python.exe" 
        self.convert_plug_args.append(self.exe)

        self.script = "ScriptFile=P:/AndreJukebox/pipe/ajbackend/rendersubmit/make_convert.py"
        self.convert_plug_args.append(self.script)

        self.pyver = "Version=3.11"
        self.convert_plug_args.append(self.pyver)

    def write_convert_plug(self):
        with open('args/convertplugin.txt','w') as output:
            for self.plugargs in self.convert_plug_args:
                output.write(self.plugargs + '\n')    

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

    def get_last_version(self,katargs,shots,layer):
        self.createdir = {}
        self.typelist = ["Katana","Nuke","mov"]
        self.all_vers = {}
        self.path_vers = {
                "Katana":f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/*',
                "Nuke":f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/nuke/*',
                "mov":f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/mov/*'
                }
        for self.ver_type in self.typelist:
            self.verfolder = glob.glob(self.path_vers[self.ver_type])
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
            self.all_vers[self.ver_type]=self.lastver
            
        self.createdir = {'Katana':f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}',
                    'Nuke':f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/nuke/{self.all_vers["Nuke"]}',
                    'mov':f'P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/mov/{self.all_vers["mov"]}'}
        
    def get_job_ids(self):
        for id in self.output.split('\r\n'):
            if id.startswith('JobID='):
                self.job = id.split('=')[1]
        self.job_id.append(self.job)

    def submit(self,katargs):
        for shotdict in katargs['shotsdict']:
            self.job_id = []
            for shots in shotdict:
                # self.generate_jobs(katargs=katargs,shots=shots,shotdict=shotdict,dcc=katargs['userdcc'])
                if katargs['userdcc'] == "Katana":
                    self.generate_jobs(katargs=katargs,shots=shots,shotdict=shotdict,dcc="Katana")

            if katargs['userdcc'] == "Nuke" or katargs['nukerender']==1:
                self.generate_jobs(katargs=katargs,shots=shots,shotdict=shotdict,dcc='Nuke')

    def generate_jobs(self,katargs,shots,shotdict,dcc):
                batchnameid = f'{katargs["seq"]}-{shots}__[{katargs["batchid"]}]'
                framestart = project_dict.proj_dict().seqsdict[katargs["seq"]][shots]['start']
                frameend = project_dict.proj_dict().seqsdict[katargs["seq"]][shots]['end']
                layer = ''
                self.currentseq = katargs["seq"]
                print(self.currentseq)
                self.nk_source = project_dict.proj_dict().seqsdict[self.currentseq][shots]["comp"]
                self.nukefile = f'P:/AndreJukebox/seq/{self.currentseq}/{self.nk_source}/comp/workfile.nk'
                if dcc == "Nuke":
                    shotdict[shots]=['write_out']
                if dcc == "mov":
                    shotdict[shots]=['ocio_convert']

                for layer in shotdict[shots]:
                    self.adr.dictread(seq=katargs['seq'],shot=shots,layer=layer)
                    self.iteration = 0
                    
                    # getting the versions #
                 
                    self.get_last_version(katargs=katargs,shots=shots,layer=layer)
                    if not os.path.exists(self.createdir[dcc]):
                        os.makedirs(self.createdir[dcc])
                    
                    if dcc=="Nuke" and katargs['makevideo']==1:
                        if not os.path.exists(self.createdir['mov']):
                            os.makedirs(self.createdir['mov'])

                    seqframes = range(int(framestart),int(frameend),1)
                    frame_len = (len(seqframes))
                    prog_step = []
                    scope = 1
                    autoprogstep = ''

                    while frame_len > 1:
                        frame_len = frame_len / 2
                        scope = scope * 2
                        prog_step.append(scope)

                    prog_step.sort(reverse = True)
                    for x in prog_step:
                        autoprogstep += f'{framestart}-{frameend}x{x},'
                    autoprogstep += f'{framestart}-{frameend}'

                    print(autoprogstep)

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
                    self.kat_jobname = f'Name={katargs["seq"]}-{shots} - {layer} - {self.all_vers["Katana"]} - ktoa render'
                    self.jobargs.append(self.kat_jobname)
                    frames = f'Frames={frames_dict[katargs["framesdict"]]}'
                    self.jobargs.append(frames)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}/beauty'
                    self.jobargs.append(outputpathrgba)
                    outputfilergba = f'OutputFilename0={layer}_beauty.####.linear.exr'
                    self.jobargs.append(outputfilergba)
                    batchname = f'BatchName={batchnameid}'
                    self.jobargs.append(batchname)
                    katver = f'EnvironmentKeyValue0=katver={self.all_vers["Katana"]}'
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
                    
                    if katargs['mode'] == "prev":
                        katargsmode="prev"
                    if "denoise" in katargs['mode']:
                        katargsmode = "denoise"
                    modevar = f'varMode=mode={katargsmode}'
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
                    comments = f'Comment=Beauty rebuild with denoised aov.'
                    self.bbo_job_args.append(comments)
                    pooluser = f'Pool=all'
                    self.bbo_job_args.append(pooluser)
                    self.bbo_name = f'Name={katargs["seq"]}-{shots} - {layer} - {self.all_vers["Katana"]} - beauty_rebuild'
                    self.bbo_job_args.append(self.bbo_name)
                    self.user = "UserName=jonnhy"
                    self.bbo_job_args.append(self.user)
                    self.frames = frames
                    self.bbo_job_args.append(self.frames)
                    self.chunk = "ChunkSize=10"
                    self.sympriority = 'Priority=90'
                    self.bbo_job_args.append(self.sympriority)                     
                    self.bbo_job_args.append(self.chunk)
                    self.bbo_job_args.append(batchname)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}/beauty'
                    self.bbo_job_args.append(outputpathrgba)
                    self.write_bbo_job()

                    ### WRITING BEAUTY REBUILD PLUGIN ARGS ###
                    self.bbo_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['Katana']} "
                    self.arguments += "<STARTFRAME>-<ENDFRAME> "
                    self.bbo_plug_args.append(self.arguments)
                    self.bbo_plug_args.append(outputpathrgba)
                    self.bbo_plug_args.append(outputfilergba)
                    self.write_bbo_plug()

                    #### WRITING DENOISE JOB
                    self.den_jobs()
                    self.den_plug = "Plugin=Python"
                    self.den_job_args.append(self.den_plug)                    
                    
                    comments = f'Comment=Denoising selected aovs with Noice'
                    self.den_job_args.append(comments)

                    pooluser = f'Pool=all'
                    self.den_job_args.append(pooluser)

                    self.den_job_args.append(batchname)
                    self.den_job_name=f'Name={katargs["seq"]}-{shots} - {layer} - {self.all_vers["Katana"]} - aov_denoise'
                    self.den_job_args.append(self.den_job_name)
                    self.den_job_args.append(self.user)
                    self.den_job_args.append(frames)
                    self.den_job_args.append(self.chunksize)
                    self.den_job_args.append(outputpathrgba)
                    self.den_job_args.append(outputfilergba)
                    self.sympriority = 'Priority=90'
                    self.den_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}/beauty'
                    self.den_job_args.append(outputpathrgba)
                    self.write_den_job()

                    #### WRITING DENOISE PLUGIN
                    self.den_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['Katana']} "
                    self.arguments += "<STARTFRAME>-<ENDFRAME> "
                    self.den_plug_args.append(self.arguments)
                    self.den_plug_args.append(outputpathrgba)
                    self.den_plug_args.append(outputfilergba)
                    self.write_den_plug()

                    #### WRITING RENAME JOB
                    self.rename_jobs()
                    self.rename_plug = "Plugin=Python"
                    self.rename_job_args.append(self.rename_plug)                    
                    
                    comments = f'Comment=Renaming aovs for denoising.'
                    self.rename_job_args.append(comments)
                    self.rename_job_args.append(batchname)
                    self.rename_job_name=f'Name={katargs["seq"]}-{shots} - {layer} - {self.all_vers["Katana"]} - aov_rename'
                    self.rename_job_args.append(self.rename_job_name)
                    self.rename_job_args.append(self.user)
                    self.framerange = f'Frames=1'
                    self.rename_job_args.append(self.framerange)
                    renchunk = len(range(int(framestart),int(frameend) + 1))
                    self.renchunksize = f'ChunkSize={renchunk}'
                    self.rename_job_args.append(self.renchunksize)
                    self.sympriority = 'Priority=90'
                    self.rename_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}/beauty'
                    self.rename_job_args.append(outputpathrgba)
                    pooluser = f'Pool=all'
                    self.rename_job_args.append(pooluser)                    
                    self.write_rename_job()

                    #### WRITING RENAME PLUGIN
                    self.rename_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['Katana']} "
                    self.arguments += f"{framestart}-{frameend} "
                    self.rename_plug_args.append(self.arguments)
                    self.rename_plug_args.append(outputpathrgba)
                    self.rename_plug_args.append(outputfilergba)
                    self.write_rename_plug()

                    #### WRITING NUKE SYM JOB
                    self.sym_jobs()
                    self.sym_plug = "Plugin=Python"
                    self.sym_job_args.append(self.sym_plug)                    
                    comments = f'Comment=Symlink "latest" to last nuke version'
                    self.sym_job_args.append(comments)
                    self.sympooluser = 'Pool=rendernode'
                    self.sym_job_args.append(self.sympooluser)
                    self.sym_job_args.append(batchname)
                    self.symnuke_job_name=f'Name={katargs["seq"]}-{shots} - {self.all_vers["Nuke"]} - Nuke - symlink'
                    self.sym_job_args.append(self.symnuke_job_name)
                    self.sym_job_args.append(self.user)
                    self.renchunksize = f'ChunkSize=1'
                    self.sym_job_args.append(self.renchunksize)
                    self.sympriority = 'Priority=90'
                    self.sym_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/nuke/latest/raw/'
                    self.sym_job_args.append(outputpathrgba)
                    self.write_symnuke_job()
                    
                    #### WRITING NUKE SYM PLUGIN
                    self.sym_plugin(dcc="Nuke")
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['Nuke']} "
                    self.arguments += f"{self.dcc} "
                    self.sym_plug_args.append(self.arguments)
                    self.sym_plug_args.append(outputpathrgba)
                    self.sym_plug_args.append(outputfilergba)
                    self.write_symnuke_plug()

                    #### WRITING SYM JOB
                    self.sym_jobs()
                    self.sym_plug = "Plugin=Python"
                    self.sym_job_args.append(self.sym_plug)                    
                    comments = f'Comment=Symlink "latest" to last version'
                    self.sym_job_args.append(comments)
                    self.sympooluser = 'Pool=rendernode'
                    self.sym_job_args.append(self.sympooluser)
                    self.sym_job_args.append(batchname)
                    self.sym_job_name=f'Name={katargs["seq"]}-{shots} - {layer} - {self.all_vers[dcc]} - {dcc} symlink'
                    self.sym_job_args.append(self.sym_job_name)
                    self.sym_job_args.append(self.user)
                    self.framerange = f'Frames=1'
                    self.sym_job_args.append(self.framerange)
                    self.renchunksize = f'ChunkSize=1'
                    self.sym_job_args.append(self.renchunksize)
                    self.sympriority = 'Priority=90'
                    self.sym_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/lgt/{layer}/{self.all_vers["Katana"]}/beauty'
                    self.sym_job_args.append(outputpathrgba)
                    self.write_sym_job()

                    #### WRITING SYM PLUGIN
                    self.sym_plugin(dcc="Katana")
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['Katana']} "
                    self.arguments += f"{self.dcc} "
                    self.sym_plug_args.append(self.arguments)
                    self.sym_plug_args.append(outputpathrgba)
                    self.sym_plug_args.append(outputfilergba)
                    self.write_sym_plug()

                    ### WRITING NUKE JOB
                    self.nuke_jobs()
                    nukeoutputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/nuke/{self.all_vers["Nuke"]}/raw'
                    self.nuke_job_args.append(nukeoutputpathrgba)
                    nukeoutputfilergba = f'OutputFilename0={shots}_linear.####.exr'
                    self.nuke_job_args.append(nukeoutputfilergba)
                    self.nuke_name=f'Name={katargs["seq"]}-{shots} - {self.all_vers["Nuke"]} - Nuke - {layer}'
                    comments = f'Comment=Nuke batch render'
                    pooluser = f'Pool={katargs["pool"]}'
                    self.nuke_job_args.append(pooluser)
                    self.nuke_job_args.append(self.nuke_name)
                    self.nuke_job_args.append(comments)
                    nukeframes = f'Frames={framestart}-{frameend}'
                    self.nuke_job_args.append(nukeframes)
                    self.nuke_job_args.append(batchname)
                    nukever = f'EnvironmentKeyValue0=nukever={self.all_vers["Nuke"]}'
                    self.nuke_job_args.append(nukever)
                    self.nukeinitialstatus = f'InitialStatus={katargs["userstatus"]}'
                    self.nuke_job_args.append(self.nukeinitialstatus)
                    self.priority = f'Priority={katargs["userpriority"]}'
                    self.nuke_job_args.append(self.priority)
                    for self.jobs in self.job_id:
                        self.dependency = f'JobDependency{self.iteration}={self.jobs}'
                        self.nuke_job_args.append(self.dependency)
                        self.iteration += 1
                    self.write_nuke_job()
                    
                    ### WRITING NUKE PLUGIN
                    self.nuke_plugin()
                    self.nukeSceneFile = f'SceneFile=P:/AndreJukebox/seq/{katargs["seq"]}/{shots}/comp/workfile.nk'
                    self.nuke_plugin_args.append(self.nukeSceneFile)
                    self.nukeWriteNode = f'WriteNode={layer}'
                    self.nuke_plugin_args.append(self.nukeWriteNode)
                    self.write_nuke_plugin()

                    ### WRITE MAKE CONVERT JOB
                    self.convert_jobs()
                    self.plugin = "Plugin=Python" 
                    self.convert_job_args.append(self.plugin)
                    comments = f'Comment=Apply ocio transforms EXR -> PNG'
                    self.convert_job_args.append(comments)
                    pooluser = f'Pool=all'
                    self.convert_job_args.append(pooluser)
                    self.convert_name = f'Name={katargs["seq"]}-{shots} - {self.all_vers["mov"]} - ocio_convert - oiiotool'
                    self.convert_job_args.append(self.convert_name)
                    self.user = "UserName=jonnhy"
                    self.convert_job_args.append(self.user)
                    self.convert_frames = f'Frames={framestart}-{frameend}'
                    self.convert_job_args.append(self.convert_frames)
                    self.chunk = "ChunkSize=10" 
                    self.sympriority = 'Priority=90'
                    self.convert_job_args.append(self.sympriority)                    
                    self.convert_job_args.append(self.chunk)
                    self.convert_job_args.append(batchname)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/nuke/{self.all_vers["Nuke"]}/temp'
                    self.convert_job_args.append(outputpathrgba)

                    self.write_convert_job()

                    ### WRITE MAKE CONVERT PLUG
                    self.convert_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{self.all_vers['Nuke']} "
                    self.arguments += "<STARTFRAME>-<ENDFRAME> "
                    self.convert_plug_args.append(self.arguments)
                    self.write_convert_plug()


                    ### WRITE MAKE VIDEO JOB
                    self.video_jobs()
                    self.plugin = "Plugin=Python" 
                    self.video_job_args.append(self.plugin)
                    comments = f'Comment=FFMPEG Apple Pro-res 422'
                    self.video_job_args.append(comments)
                    pooluser = f'Pool=all'
                    self.video_job_args.append(pooluser)
                    self.video_name = f'Name={katargs["seq"]}-{shots} - {self.all_vers["mov"]} - ffmpeg - create_mov'
                    self.video_job_args.append(self.video_name)
                    self.user = "UserName=jonnhy"
                    self.video_job_args.append(self.user)
                    self.framerange = f'Frames=1'
                    self.sym_job_args.append(self.framerange)
                    self.video_job_args.append(batchname)
                    self.sympriority = 'Priority=90'
                    self.video_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/mov/{self.all_vers["mov"]}/'
                    self.video_job_args.append(outputpathrgba)
                    self.write_video_job()
                    

                    ### WRITE MAKE VIDEO PLUG
                    self.video_plugin()
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{self.all_vers['mov']} "
                    self.video_plug_args.append(self.arguments)
                    self.write_video_plug()                    
                    
                    ### WRITE MAKE SYM VIDEO JOB
                    self.sym_jobs()
                    self.sym_plug = "Plugin=Python"
                    self.sym_job_args.append(self.sym_plug)                    
                    comments = f'Comment=Symlink creation for the latest video'
                    self.sym_job_args.append(comments)
                    self.sympooluser = 'Pool=rendernode'
                    self.sym_job_args.append(self.sympooluser)
                    self.sym_job_args.append(batchname)
                    self.sym_videojob_name=f'Name={katargs["seq"]}-{shots} - {self.all_vers["mov"]} - mov - symlink'
                    self.sym_job_args.append(self.sym_videojob_name)
                    self.sym_job_args.append(self.user)
                    self.renchunksize = f'ChunkSize=1'
                    self.sym_job_args.append(self.renchunksize)
                    self.sympriority = 'Priority=90'
                    self.sym_job_args.append(self.sympriority)
                    outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{katargs["seq"]}/{shots}/mov/latest/'
                    self.sym_job_args.append(outputpathrgba)
                    self.write_symvideo_job()

                    #### WRITING SYM VIDEO PLUGIN
                    self.sym_plugin(dcc="Katana")
                    self.arguments = "Arguments="
                    self.arguments += f"{katargs['seq']} "
                    self.arguments += f"{shots} "
                    self.arguments += f"{layer} "
                    self.arguments += f"{self.all_vers['mov']} "
                    self.arguments += f"mov "
                    self.sym_plug_args.append(self.arguments)
                    self.sym_plug_args.append(outputpathrgba)
                    self.sym_plug_args.append(outputfilergba)
                    self.write_symvideo_plug()

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

                    self.renamejob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/renamejob.txt'
                    self.renameplugin = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/renameplugin.txt'

                    self.symjob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symjob.txt'
                    self.symplugin = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symplugin.txt'

                    self.symnukeplug = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symnukeplugin.txt'
                    self.symnukejob = 'P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symnukejob.txt'

                    self.nukejob = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/nukejob.txt"
                    self.nukeplugin = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/nukeplugin.txt"
                    self.nuke_aux = self.nukefile

                    self.convertjob = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/convertjob.txt"
                    self.convertplugin = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/convertplugin.txt"
                    
                    self.videojob = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/videojob.txt"
                    self.videoplugin = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/videoplugin.txt"

                    self.videosymjob = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symvideojob.txt"
                    self.videosymplugin = "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/symvideoplugin.txt"
                    
                    # GENERATING THE ARGS.TXT for multiple job submission
                    self.args.append(self.submitjobs)
                    self.args.append(self.dep)

                    if dcc == "Katana":
                        # katana job
                        print('_____________________________________')
                        print('KATANA RENDER - RENDER LAYER')
                        if katargs['mode'] == "prev" or katargs['mode'] == "denoise":
                            self.args.append(self.job)
                            self.args.append(self.katjob)
                            self.args.append(self.katplug)
                            self.args.append(self.katfile)
                            print(self.kat_jobname)

                        # rename job
                        if katargs['mode'] == "denoise" or katargs['mode'] == "denoise_only":
                            if not len(self.adr.aovdict)==0:
                                self.args.append(self.job)
                                self.args.append(self.renamejob)
                                self.args.append(self.renameplugin)
                                print(self.rename_job_name)

                        # denoise job
                        if katargs['mode'] == "denoise" or katargs['mode'] == "denoise_only":
                            if not len(self.adr.aovdict)==0:
                                self.args.append(self.job)
                                self.args.append(self.denjob)
                                self.args.append(self.denplug)
                                print(self.den_job_name)


                        # beauty rebuild job
                        if katargs['mode'] == "denoise" or katargs['mode'] == "denoise_only":
                            if not len(self.adr.aovdict)==0:
                                self.args.append(self.job)
                                self.args.append(self.beautyjob)
                                self.args.append(self.beautyplug)
                                print(self.bbo_name)

                        if katargs['makesym']==1:
                            self.args.append(self.job)
                            self.args.append(self.symjob)
                            self.args.append(self.symplugin)
                            print(self.sym_job_name)


                    if dcc == "Nuke":
                        print('_____________________________________')
                        print('NUKE RENDER - EXR OUTPUT')
                        self.args.append(self.job)
                        self.args.append(self.nukejob)
                        self.args.append(self.nukeplugin)
                        self.args.append(self.nuke_aux)
                        print(self.nuke_name)

                        #symlink job
                        if katargs['makesym']==1:
                            self.args.append(self.job)
                            self.args.append(self.symnukejob)
                            self.args.append(self.symnukeplug)
                            print(self.symnuke_job_name)
                        


                    if dcc=="Nuke" and katargs['makevideo']==1:
                        print('_____________________________________')
                        print('OCIO CONVERT - EXR --> PNG and FFMPEG MOVE CREATION')
                        self.args.append(self.job)
                        self.args.append(self.convertjob)
                        self.args.append(self.convertplugin)
                        print(self.convert_name)

                        
                        self.args.append(self.job)
                        self.args.append(self.videojob)
                        self.args.append(self.videoplugin)
                        print(self.video_name)

                        if katargs['makesym']==1:
                            self.args.append(self.job)
                            self.args.append(self.videosymjob)
                            self.args.append(self.videosymplugin)
                            print(self.sym_videojob_name)
                    
                    self.write_multiple_args()
                    

                    multiplecommand = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/args/args.txt"'
                    self.response = subprocess.Popen(multiplecommand, stdout=subprocess.PIPE)
                    self.output = self.response.communicate()[0].decode()

                    if katargs['userdcc'] == "Katana":
                        self.get_job_ids()
    print('__________________________________________________________________')