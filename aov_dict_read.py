import json

class aov_dict():
    def __init__(self):
        pass

    def dictread(self,seq,shot,layer):
        self.jsonpath = f'P:/AndreJukebox/seq/{seq}/{shot}/products/aovdict/{layer}.json'
        self.aovjson = open(self.jsonpath, "r")
        self.aovdict = json.load(self.aovjson)

# aov_dict().dictread(seq='010_NCT',shot='s0100',layer='base_all')