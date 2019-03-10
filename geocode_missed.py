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

        d = pd.read_csv(base+'missed_inst.csv',dtype=str)

        for i,nm in zip(d['id_inst'],d['nm_inst']):
            url = baseurl.format(nm)
            yield scrapy.Request(url=url,callback=self.parse,meta={'id_inst':str(i),'nm_inst':nm})

    def parse(self, response):
        id_inst = response.meta['id_inst']
        nm_inst = response.meta['nm_inst']
        base = '/Users/chjiang/GitHub/collaboratenet/'

        with open(base+'geocode_missed/{}.json'.format(id_inst), 'wb') as f:
            f.write(response.body)
            yield {'name': nm_inst}
