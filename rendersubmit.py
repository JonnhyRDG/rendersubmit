import json
import subprocess

class rendersubmit():
    def __init__(self):
        self.dictread()

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)

    # jobs file
    def joboptions(self,seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk):
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
    
    
    
    
    def submit(self,seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk):
        for shots in shotsdict:
            framestart = self.seqsdict[seq][shots]['start']
            frameend = self.seqsdict[seq][shots]['end']
            for layer in shotsdict[shots]:
                # ---- writing jobs file
                self.joboptions(seq,shotsdict,userdcc,userstatus,usercomment,userpriority,userchunk)
                jobname = f'Name={seq}-{shots} - {layer}'
                self.jobargs.append(jobname)
                frames = f'Frames={framestart}-{frameend}'
                self.jobargs.append(frames)
                
                outputpathrgba = f'OutputDirectory0=P:/AndreJukebox_output/renders/concept_animatic/{seq}/{shots}/lgt/{layer}/latest/rgba'
                self.jobargs.append(outputpathrgba)
                
                outputfilergba = f'OutputFilename0={layer}_rgba.####.linear.exr'
                self.jobargs.append(outputfilergba)
                
                outputpath = f'OutputDirectory1=P:/AndreJukebox_output/renders/concept_animatic/{seq}/{shots}/lgt/{layer}/latest'
                self.jobargs.append(outputpath)
                
                batchname = f'BatchName={seq}-{shots}'
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

                # # ---- writing cmds file
                # self.cmdsoptions()
                # seqvar = f'--var shot={seq}'
                # self.cmdsargs.append(seqvar)
                # shotvar = f'--var shot={shots}'
                # self.cmdsargs.append(shotvar)
                # layervar = f'--var shot={layer}'
                # self.cmdsargs.append(layervar)
                # renderfile = f'"P:/AndreJukebox/seq/{seq}/{shots}/lighting/shot.katana"'
                # self.cmdsargs.append(renderfile)
                # self.writecmds()

                command = f'deadlinecommand "P:/AndreJukebox/pipe/ajbackend/rendersubmit/jobs.txt" "P:/AndreJukebox/pipe/ajbackend/rendersubmit/plugins.txt" "P:/AndreJukebox/seq/{seq}/{shots}/lighting/shot.katana"'
                subprocess.call(command, shell=True)
                # command = f'deadlinecommand -SubmitCommandLineJob -prop Comment="{usercomment}" -priority "{userpriority}" -chunksize "{userchunk}" -executable "P:\AndreJukebox\pipe\katana4.bat" -name "{seq}_{shots} - {layer}" -initialstatus "{userstatus}" -arguments "--batch --katana-file=""P:\AndreJukebox\seq\{seq}\{shots}\lighting\shot.katana"" --render-node={layer} " -frames {framestart}-{frameend}'
                
                # -prop -BatchName="{seq}-{shots}"