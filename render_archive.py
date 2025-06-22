import os
import glob
import subprocess
import project_dict

pd = project_dict.proj_dict()
pd.dictread()


exclude = ['vfx','anim','cfx']
def copy_folders(seq,shot):
    source_product_path = f'P:\\AndreJukebox\\seq\\{seq}\\{shot}\\products\\'
    source_prod_type = glob.glob(f'{source_product_path}\\*')

    for source_folders in source_prod_type:
        if os.path.isdir(source_folders):
            dest_folders = source_folders.replace('P:','H:')
            if all(x not in dest_folders for x in exclude):
                copycmd = f'xcopy /Y {source_folders} {dest_folders}\\'
                subprocess.call(copycmd,shell=True)
            
                if not os.path.exists(dest_folders):
                    os.makedirs(os.path.abspath(dest_folders))
                else:
                    print(f'{dest_folders} already exists')
            else:
                type_items = glob.glob(f'{source_folders}\\*')
                ver_source_list=[]
                for assets in type_items:
                    if os.path.isdir(assets):
                        versions = glob.glob(f'{assets}\\*')
                        for ver in versions:
                            if os.path.islink(ver):
                                linked_ver = os.path.realpath(ver).replace("\\\Workstation02\\p\\","P:\\")
                                ver_source_list.append(linked_ver)
                for lastver in ver_source_list:
                    source = lastver
                    dest = source.replace('P:\\','H:\\')
                    copycmd = f'xcopy /Y {source} {dest}\\'
                    subprocess.call(copycmd,shell=True)
                    
                    assetdir = dest.rsplit("\\",1)[0]
                    destver = f'{assetdir}\latest'
                    if not os.path.exists(destver):
                        os.rename(dest,destver)

for seqs in pd.seqsdict:
    for shots in pd.seqsdict[seqs]:
        copy_folders(seqs,shots)