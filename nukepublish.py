import sys, nuke
import os

from rendersubmit import rendersubmit
import customread
import gsv


# import dead

def openscript(seq,key):
    file = f'P:/AndreJukebox/seq/{seq}/{key}/comp/workfile.nk'
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
    savefile = f'P:/AndreJukebox/seq/{seq}/{shot}/comp/workfile.nk'
    nuke.scriptSave(savefile) #('P:/AndreJukebox_output/comp/concept_animatic/020_MFG/s0270/workfile.nk') #save the child key


openscript(seq=sys.argv[1],key=sys.argv[3])
updategsv(seq=sys.argv[1],shot=sys.argv[2])
savescript(seq=sys.argv[1],shot=sys.argv[2])

# from Deadline import Groups
# from Deadline import DeadlineConnect

# from Deadline import DeadlineConnect as Connect
# con = Connect.DeadlineCon('localhost', 8081)
# print(con.Groups.GetGroupNames())

# connectionobjet = DeadlineConnect.DeadlineCon

# groups = Groups.Groups().GetGroupNames()
# print(groups)
