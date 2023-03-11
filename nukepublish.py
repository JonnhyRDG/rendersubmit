import sys, nuke
import os

from rendersubmit import rendersubmit
import customread
import gsv
# from DeadlineNukeClient import DeadlineCon as Connect
# con = Connect('WebServiceName', 8081)
# con.Groups.GetGroupNames()

def openscript(seq,key):
    file = f'P:/AndreJukebox_output/comp/concept_animatic/{seq}/{key}/workfile.nk'
    nuke.scriptOpen(file) #('P:/AndreJukebox_output/comp/concept_animatic/020_MFG/s0260/workfile.nk') load the key script

def updategsv(seq,shot):
    nuke.root().knobs()['shots'].setValue(shot) #nuke.root().knobs()['shots'].setValue('s0270')
    shotnew = nuke.root().knobs()['shots'].value()
    reads = nuke.allNodes() #replace for loop selecting all nodes with knobs 'customreadclass'
    for customs in reads:
        if customs.knob('customreadclass'):
            print(customs.name())
            customs.knobs()['shot'].setValue(shotnew) # this is going to happen in the createfunc loop. Read this from the root.
            customs.knobs()['populate'].execute()
            customs.knobs()['version'].setValue('latest')
            customs.knobs()['create'].execute() #replace with for loop and execute createfunc.
        else:
            continue

def savescript(seq,shot):
    savefile = f'P:/AndreJukebox_output/comp/concept_animatic/{seq}/{shot}/workfile.nk'
    nuke.scriptSave(savefile) #('P:/AndreJukebox_output/comp/concept_animatic/020_MFG/s0270/workfile.nk') #save the child key


openscript(seq=sys.argv[1],key=sys.argv[3])
updategsv(seq=sys.argv[1],shot=sys.argv[2])
savescript(seq=sys.argv[1],shot=sys.argv[2])
