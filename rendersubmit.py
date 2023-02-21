import json
import subprocess

class rendersubmit():
    def __init__(self):
        self.dictread()

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)


    def submit(self):
        # seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        # seqsdict = json.load(seqsdictjson)        
        comment = "automated submit test"
        seq = "010_NCT"
        shot = ['s0010','s0020','s0130','s0250','s0115']
        framestart = 1001
        frameend = 1218
        layer = 'env_all'
        status = 'Suspended'
        dcc = 'katana'

        for shots in shot:
            framestart = self.seqsdict[seq][shots]['start']
            frameend = self.seqsdict[seq][shots]['end']
            command = f'deadlinecommand -SubmitCommandLineJob -prop Comment="{comment}" -executable "P:\AndreJukebox\pipe\katana4.bat" -name "{seq}_{shots} - {layer} - {dcc}" -initialstatus "{status}" -arguments "P:\AndreJukebox\seq\{seq}\{shots}\lighting\shot.katana" -frames {framestart}-{frameend}'
            subprocess.call(command, shell=True)

rendersubmit().submit()