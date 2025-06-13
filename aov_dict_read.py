import json

class aov_dict():
    def __init__(self):
        pass

    def dictread(self,seq,shot,layer):
        self.jsonpath = f'P:/AndreJukebox/seq/{seq}/{shot}/products/aovdict/{layer}.json'
        self.aovjson = open(self.jsonpath)
        self.aovdict = json.load(self.aovjson)
        