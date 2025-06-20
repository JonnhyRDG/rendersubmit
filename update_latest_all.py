import os
import glob
import subprocess

seqs = []
seqpath = f'P:/AndreJukebox_output/renders/concept_animatic/'
seqglob = glob.glob(f'{seqpath}*')
for seq in seqglob:
    seqs.append(os.path.abspath(seq))

layervers = {}
shots = []
for sequences in seqs:
    shotspaths = glob.glob(f'{sequences}/*')
    for shot in shotspaths:
        shots.append(os.path.abspath(shot))

types = []
layerpaths = []

def get_types(path):
    typepath = glob.glob(path)
    for shotpath in typepath:
        typepaths = glob.glob(f'{shotpath}/*')
        for tp in typepaths:
            types.append(tp)
            if not "lgt" in tp:
                layerpaths.append(tp)

def get_layers(path):
        if 'lgt' in path:
            layers = glob.glob(os.path.abspath(f'{path}/*'))
            for items in layers:
                layerpaths.append(items)

def get_versions(path):
    latest_folder = f'{path}\\latest'
    if os.path.exists(latest_folder):
        delcommand = f'rmdir {latest_folder}'
        subprocess.call(delcommand,shell=True)
    versions = glob.glob(f'{path}/*')
    print(path)
    try:
        lastver = os.path.abspath(versions[-1])
    except:
        pass
    
    try:
        symcommand = f'mklink /D {latest_folder} {lastver}'
        subprocess.call(symcommand,shell=True)
    except:
        pass
    
for s in shots:
    get_types(s)
for t in types:
    get_layers(t)
for l in layerpaths:
    get_versions(l)
