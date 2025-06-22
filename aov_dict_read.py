import json
import os

class aov_dict():
    def __init__(self):
        pass

    def dictread(self,seq,shot,layer):
        self.jsonpath = f'P:/AndreJukebox/seq/{seq}/{shot}/products/aovdict/{layer}.json'
        if not os.path.exists(self.jsonpath):
            self.aovdict = {}
        else:
            self.aovjson = open(self.jsonpath, "r")
            self.aovdict = json.load(self.aovjson)
        return self.aovdict

# ad = aov_dict()
# ad.dictread(seq='010_NCT',shot='s0100',layer='base_vol')
# print(ad.aovdict)
