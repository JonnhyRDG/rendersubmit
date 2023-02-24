import json
import subprocess

class rendersubmit():
    def __init__(self):
        self.dictread()

    def dictread(self):
        self.seqsdictjson = open('P:/AndreJukebox/aj_seq_dict.json')
        self.seqsdict = json.load(self.seqsdictjson)


    def submit(self,seq,shotsdict):
        comment = "automated submit"
        status = 'Suspended'
        dcc = 'katana'

        for shots in shotsdict:
            framestart = self.seqsdict[seq][shots]['start']
            frameend = self.seqsdict[seq][shots]['end']
            for layer in shotsdict[shots]:
                command = f'deadlinecommand -SubmitCommandLineJob -prop Comment="{comment}" -executable "P:\AndreJukebox\pipe\katana4.bat" -name "{seq}_{shots} - {layer} - {dcc}" -initialstatus "{status}" -arguments "P:\AndreJukebox\seq\{seq}\{shots}\lighting\shot.katana" -frames {framestart}-{frameend}'
                subprocess.call(command, shell=True)