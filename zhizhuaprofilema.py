import scrapy

import numpy as np
import pandas as pd

class PaperProfile(scrapy.Spider):
    name = "AProfile"
    
    base = '/Users/chjiang/GitHub/collaboratenet/'
    authorship = pd.read_csv(base+'authorshipma.csv', dtype=str)
    aids = np.unique(authorship['id_auth'])
  
    start_urls = []
    
    for aid in aids:
        url = "https://preview.academic.microsoft.com/api/entity/author/{}?paperId=undefined".format(aid)
        start_urls.append(url)

    def parse(self, response):
        url = response.url
        idx1, idx2 = url.rfind('/'), url.find('?')
        aid = url[idx1+1:idx2]
	
        base = '/Users/chjiang/GitHub/collaboratenet/'
        with open(base+'aidma/{}.json'.format(aid), 'wb') as f:
            f.write(response.body)

