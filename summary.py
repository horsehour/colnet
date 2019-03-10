def extract_geolocs():
    base = '/Users/chjiang/GitHub/collaboratenet/'

    authorsma = pd.read_csv(base+'authorsma.csv',dtype=str)
    authorsma.fillna('',inplace=True)

    authorship = pd.read_csv(base+'authorshipma.csv',dtype=str)
    authorship.fillna('', inplace=True)

    selected = authorship[authorship['nm_inst'].apply(len) == 0]['id_auth']
    noaff = []
    for auth in set(selected.values):
        group = authorship[authorship['id_auth'] == auth]
        if np.all(group['nm_inst'].apply(len) == 0):
            noaff.append(auth)

    nm_inst1 = set(authorship['nm_inst'])
    nm_inst2 = set(authorsma[authorsma['id_auth'].isin(noaff) & (authorsma['nm_inst'].apply(len) > 0)]['nm_inst'])

    insts = list(nm_inst1.union(nm_inst2))



    d1=authorship[authorship['nm_inst'].isin(insts)][['id_inst','nm_inst']]
    d2=authorsma[authorsma['nm_inst'].isin(insts)][['id_inst','nm_inst']]
    d=pd.concat([d1,d2])
    d.drop_duplicates(inplace=True)
    d=d[d['nm_inst'].apply(len) > 0]

    lats,lngs = [],[]
    count = 0
    for i,nm in zip(d['id_inst'],d['nm_inst']):
        if not i:
            count +=1
            i = count

        file = base+'geocode/{}.json'.format(i)
    #     if not os.path.exists(file):
    #         continue

        with open(file,'r') as f:
            loc = json.load(f)['results']
            if len(loc) == 0:
                print(i,nm)
                lat,lng = '',''
            else:
                loc=loc[0]['geometry']['location']
                lat,lng=loc['lat'],loc['lng']
            lats.append(lat)
            lngs.append(lng)

        f.close()

    d['lat'] = lats
    d['lng'] = lngs
    d.to_csv(base+'geoloc_inst.csv',index=False)
    

def build_collaborate_network():
    geoloc=pd.read_csv(base+'geoloc_inst.csv',dtype=str)

    authorsma = pd.read_csv(base+'authorsma.csv',dtype=str)
    authorsma.fillna('',inplace=True)

    authorship = pd.read_csv(base+'authorshipma.csv',dtype=str)
    authorship.fillna('', inplace=True)

    grp1=authorship[['id_auth','nm_auth','id_inst','nm_inst']]
    authorsma=authorsma[authorsma['id_auth'].isin(grp1['id_auth'])]
    grp2=authorsma[['id_auth','nm_auth','id_inst','nm_inst']]

    grp=pd.concat([grp1,grp2])
    grp.drop_duplicates(subset=['id_auth','nm_inst'], inplace=True)

    auth_inst=grp[grp['nm_inst'].apply(len) > 0]

    nm_inst2 = geoloc['nm_inst']
    cross_indices = []
    for nm in auth_inst['nm_inst']:
        indices = np.where(nm_inst2 == nm)
        if len(indices[0])>0:
            cross_indices.append(indices[0][0])
        else:
            print(nm)

    auth_inst['lat'] = list(geoloc['lat'][cross_indices])
    auth_inst['lng'] = list(geoloc['lng'][cross_indices])

    import itertools
    p_grp = authorship.groupby(by='pid').groups
    pairs=set()
    for pid in p_grp:
        coauths = p_grp[pid]
        if len(coauths) == 1:
            continue

        for a1,a2 in itertools.product(coauths,coauths):
            if a1 == a2:
                continue
            if ((a1,a2) in pairs) or ((a2,a1) in pairs):
                continue
            pairs.add((a1,a2))

    rids = pd.DataFrame(list(pairs),columns=['r1','r2'])
    id_auths = authorship['id_auth']
    coauthship = pd.DataFrame(list(id_auths[rids['r1']]),columns=['id_auth1'])
    coauthship['id_auth2'] = list(id_auths[rids['r2']])
    # all possible coauthorship between two different authors w.r.t their author id
    coauthship.drop_duplicates(inplace=True)

    collaborate_net = []
    # because each author may have changed multiple affiliation, thus rebuiding the 
    # coauthorship between the institutions
    auth_inst=auth_inst.reset_index(drop=True)
    a_grp = auth_inst.groupby(by='id_auth').groups
    for a1,a2 in zip(coauthship['id_auth1'],coauthship['id_auth2']):
        if ((a1 not in a_grp) or (a2 not in a_grp)):
            print(a1,a2)
            continue

        for r1,r2 in zip(a_grp[a1],a_grp[a2]):
            collaborate_net.append(np.hstack([auth_inst.iloc[r1],auth_inst.iloc[r2]]))
    collaborate_net = pd.DataFrame(collaborate_net,columns=['id_auth1','nm_auth1','id_inst1','nm_inst1','lat1','lng1','id_auth2','nm_auth2','id_inst2','nm_inst2','lat2','lng2'])
    collaborate_net.to_csv(base+'collaborate.csv',index=False)