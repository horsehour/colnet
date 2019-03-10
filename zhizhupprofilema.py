import scrapy

import numpy as np
import pandas as pd

class PaperProfile(scrapy.Spider):
    name = "PProfile"
    
    base = ''
    papers = pd.read_json(base+'papersma.json')
    papers = np.unique(papers.paper)
  
    start_urls = []
    
    for paper in papers:
        pid = ''.join([s for s in paper if s.isdigit()])
        url = "https://preview.academic.microsoft.com/api/entity/{}?entityType=2".format(pid)
        start_urls.append(url)

#    start_urls = [
#        "https://preview.academic.microsoft.com/api/entity/1502203205?entityType=2",
#        "https://preview.academic.microsoft.com/api/entity/author/2132226381?paperId=undefined"
#    ]

    def parse(self, response):
        url = response.url
        idx1, idx2 = url.rfind('/'), url.find('?')
        pid = url[idx1+1:idx2]
	
        base = '.'
        with open(base+'pidma/{}.json'.format(pid), 'wb') as f:
            f.write(response.body)

