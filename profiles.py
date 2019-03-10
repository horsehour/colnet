import pandas as pd
import numpy as np

from glob import glob
import json


def get_authorship():
    profiles = []

    for file in glob('pidma/*.json'):
        with open(file,'r') as f:
            data_paper = json.load(f)

        pid = file[file.rfind('/')+1:-5]
        authors=data_paper['entity']['authors']
        coauths = []
        for auth in authors:
            curr_inst = auth['currentInstitution']
            id_inst, nm_inst = '',''
            if 'displayName' in curr_inst:
                id_inst = curr_inst['id']
                nm_inst = curr_inst['displayName']
            id_auth, nm_auth = auth['id'], auth['displayName']
            profiles.append((pid, id_inst,nm_inst,id_auth,nm_auth))

    df = pd.DataFrame(profiles,columns=['pid','id_inst','nm_inst','id_auth','nm_auth'])
    df.to_csv('authorshipma.csv',index=False)

def get_authors():
    profiles = []

    for file in glob('aidma/*.json'):
        with open(file,'r') as f:
            data_auth = json.load(f)

        aid = file[file.rfind('/')+1:-5]
        auth=data_auth['entity']
        if 'currentInstitution' in auth:
            curr_inst = auth['currentInstitution']
            id_inst, nm_inst = curr_inst['id'],curr_inst['displayName']
            profiles.append((aid,auth['displayName'],id_inst,nm_inst))

    df = pd.DataFrame(profiles,columns=['id_auth','nm_auth','id_inst','nm_inst'])
    df.to_csv('authorsma.csv',index=False)

#get_authorship()
get_authors()
    
