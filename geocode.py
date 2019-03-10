import numpy as np
import pandas as pd

import scrapy

class ZhiZhuGeocode(scrapy.Spider):
    name = "ZhiZhuGeocode"
    custom_settings = {
        'DOWNLOAD_DELAY': 0.25
    }

    def start_requests(self):
        baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyD90Mkypw-O7LX6DLU-khrqt8Drj_vEvIY'

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
        
        did = []
        count = 0
        for i,nm in zip(d['id_inst'],d['nm_inst']):
            if not i:
                count +=1
                i = count

            did.append(i)
            url = baseurl.format(nm)
            yield scrapy.Request(url=url,callback=self.parse,meta={'id_inst':str(i),'nm_inst':nm})

    def parse(self, response):
        id_inst = response.meta['id_inst']
        nm_inst = response.meta['nm_inst']
        base = '/Users/chjiang/GitHub/collaboratenet/'

        with open(base+'geocode/{}.json'.format(id_inst), 'wb') as f:
            f.write(response.body)
            yield {'name': nm_inst}
