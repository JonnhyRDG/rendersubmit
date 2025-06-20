import sys, nuke
import os
import glob
import subprocess

from rendersubmit import rendersubmit
import customread
import gsv


def openscript(seq,key):
    file = f'P:/AndreJukebox/seq/{seq}/{key}/comp/workfile.nk'
    nuke.scriptOpen(file) #('P:/AndreJukebox_output/comp/concept_animatic/020_MFG/s0260/workfile.nk') load the key script
    


def archive(seq,key):
    folder = f'P:\\AndreJukebox\\seq\\{seq}\\{key}\\comp\\'
    file = 'workfile.nk'
    full_nk_path = f'{folder}{file}'
    archive_path = f'{folder}archive\\'
    if not os.path.exists(archive_path):
        os.mkdir(archive_path)

    versions = glob.glob(f'{archive_path}*')
    lastver = versions[-1]
    # new_last_ver = f"{lastver.rsplit('/',1)}/{int(lastver.rsplit('/')[-1])+1}"
    new_last_ver = int(lastver.rsplit('\\',1)[1])+1
    new_last_ver_path = f'{archive_path}{new_last_ver:04d}\\{file}'
    full_nk_path_time = os.path.getmtime(full_nk_path)
    lastver_time = os.path.getmtime(f'{lastver}/{file}')
    if full_nk_path_time > lastver_time:
        os.makedirs(f'{archive_path}{new_last_ver:04d}')
        copycmd = f'copy {full_nk_path} {new_last_ver_path}'
        subprocess.call(copycmd,shell=True)
        print(full_nk_path)
        print(new_last_ver_path)
    else:
        print(f"{key} already done.")

def updategsv(seq,shot):
    print(f"this is the shot passing {shot}")
    nuke.root().knobs()['shots'].setValue(shot) #nuke.root().knobs()['shots'].setValue('s0270')
    seqnew = nuke.root().knobs()['seqs'].value()
    shotnew = nuke.root().knobs()['shots'].value()
    reads = nuke.allNodes("Group") #replace for loop selecting all nodes with knobs 'customreadclass'

    for customs in reads:
        if customs.knob('customreadclass'):
            layer = customs.knob("layer").value()
            layerpath = f'P:/AndreJukebox_output/renders/concept_animatic/{seq}/{shot}/lgt/{layer}'
            if not os.path.exists(layerpath):
                print(layerpath," does not exist, skipping and disabling")
                customs.knob("disable").setValue(1)
            else:
                print(layerpath, "layer found, updating!")
                customs.knobs()['seq'].setValue(seqnew)
                customs.knobs()['shot'].setValue(shotnew) # this is going to happen in the createfunc loop. Read this from the root.
                customs.knobs()['populate'].execute()
                customs.knobs()['layer'].setValue(layer)
                customs.knobs()['version'].setValue('latest')
                customs.knobs()['create'].execute() #replace with for loop and execute createfunc.
        else:
            continue

def savescript(seq,shot):
    savefile = f'P:/AndreJukebox/seq/{seq}/{shot}/comp/workfile.nk'
    nuke.scriptSave(savefile) #('P:/AndreJukebox_output/comp/concept_animatic/020_MFG/s0270/workfile.nk') #save the child key

seq=sys.argv[1]
key=sys.argv[3]
shot=sys.argv[2]

archive(seq,key)
openscript(seq,key)
updategsv(seq,shot)
savescript(seq,shot)