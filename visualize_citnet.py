#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Chunheng Jiang (jiangchunheng@gmail.com)
# Created at 11:36 PM Jan 15, 2019

import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap, PowerNorm

def plot_map():
    base = '/Users/chjiang/GitHub/collaboratenet/'
    
    df = pd.read_csv(base+'collaborate.csv')
    links=df[['lat1','lng1','lat2','lng2']]
    links.drop_duplicates(inplace=True)
    
    plt.figure(figsize=(27, 20))

    m = Basemap(projection='merc',llcrnrlat=-50,llcrnrlon=-130,urcrnrlat=80,urcrnrlon=160)
    m.drawcoastlines(color=[.95,.64,.20,1.0], linewidth=1.5)
    m.drawmapboundary(fill_color=[1.0,1.0,1.0,1.0])

    vips = ['Jianxi Gao', 'Xiaozheng He', 'Lazaros K. Gallos']
    lat_lng = [(42.730172,-73.67880300000002),(42.730172,-73.67880300000002),(40.6670739,-73.9522688)]
    vips.append('Nina H. Fefferman')
    lat_lng.append((40.5008186,-74.44739910000001))
    vips.append('Shlomo Havlin')
    lat_lng.append((32.0691989,34.8430876))
    vips.append('Reuven Cohen')
    lat_lng.append((32.0691989,34.8430876))
    vips.append('Efrat Blumenfeld-Lieberthal')
    lat_lng.append((32.7767783,35.0231271))
    vips.append('Nimrod Serok')
    lat_lng.append((32.1133141,34.8043877))
    lat_lng.append((42.3504997,-71.1053991))
    lat_lng.append((39.984492,116.348175))
    lat_lng.append((40.85067249999999,-73.9295149))
    lat_lng.append((50.5804673,8.6771403))

    lat_lng=np.array(lat_lng)
    x1,x2=m(lat_lng[:,1],lat_lng[:,0])

    m.plot(x1,x2,'ro',markersize=15,alpha=0.6)
    
    names=['Gao & He', 'Fefferman & Gallos', 'Havlin & Cohen', 'Blumenfeld-Lieberthal & Serok', 'Daqing Li', 'H. Eugene Stanley', 'Sergey V. Buldyrev','Armin Bunde']
    lat_lng=np.array([[40,-70],[38,-70],[28,32],[35,32], [38,115],[43,-71],[46,-85],[51,9]])
    x1,x2=m(lat_lng[:,1],lat_lng[:,0])
    for z1,z2,name in zip(x1,x2,names):
        plt.text(z1,z2,name,fontsize=15,color='k')

    ec_rpi,ec_bar_ilan,ec_nyu,ec_tel_aviv=[.8,.21,.17,1],[.98,.88,.86,1],[.95,.64,.51,1],[.57,.77,.87,1]
    lat_edu = [42.730172,32.0691989,40.6670739,32.1133141]
    ec = [.15,.25,.56,.5]
    
    for i, link in enumerate(links.iterrows()):
        link = link[1]

        cc = ec
#         lats = [link['lat1'],link['lat2']]
#         if lat_edu[0] in lats:
#             cc=ec_rpi
#         elif lat_edu[1] in lats:
#             cc=ec_bar_ilan
#         elif lat_edu[2] in lats:
#             cc=ec_nyu
#         elif lat_edu[3] in lats:
#             cc=ec_tel_aviv

        line, = m.drawgreatcircle(link['lng1'], link['lat1'],
                                  link['lng2'], link['lat2'],
                                  linewidth=.5, color=cc)

        # if the path wraps the image, basemap plots a nasty line connecting
        # the points at the opposite border of the map.
        # we thus detect path that are bigger than 30km and split them
        # by adding a NaN

        path = line.get_path()
        cut_point, = np.where(np.abs(np.diff(path.vertices[:, 0])) > 30000e3)
        if len(cut_point) > 0:
            cut_point = cut_point[0]
            vertices = np.concatenate([path.vertices[:cut_point,:],
                                      [[np.nan, np.nan]],
                                      path.vertices[cut_point+1:,:]])

            path.codes = None
            # treat vertices as a serie of line segments
            path.vertices = vertices
    
    lat_lng = np.vstack([df[['lat1','lng1']],df[['lat2','lng2']]])
    x1,x2=m(lat_lng[:,1],lat_lng[:,0])
    plt.scatter(x1,x2,color='b',s=10)
    plt.savefig(base+'academicit3.png', format='png', bbox_inches='tight')

if __name__ == '__main__':    
    plot_map()