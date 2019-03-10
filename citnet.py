#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Chunheng Jiang (jiangchunheng@gmail.com)


from graph_tool.all import *

import pandas as pd
import numpy as np


def setup_cocite_net():
    base = ''
    authors = pd.read_json(base + 'coauths.json')
    # parse cocite connections
    links = set()
    for auth in authors.auths:
        coauths = auth.split(',')
        if len(coauths) == 1:
            continue
            
        coauths = [coauth.strip() for coauth in coauths]
        for i in range(1,len(coauths)):
            links.add((coauths[0], coauths[i]))
    links = set(links)

    node_index, edges = {}, {}

    G = Graph(directed=False)
    node_names = G.new_vp('string')

    for n1,n2 in links:
        if n1 not in node_index:
            v1 = G.add_vertex()
            node_index[n1] = v1
            node_names[v1] = n1
        else:
            v1 = node_index[n1]

        if n2 not in node_index:
            v2 = G.add_vertex()
            node_index[n2] = v2
            node_names[v2] = n2
        else:
            v2 = node_index[n2]

        e = G.add_edge(v1,v2)
        edges[(v1,v2)] = e
    return node_names, node_index, edges, G


def layout(G, node_names, node_index, pos_file, layout_algo='sfdp'):
    if pos_file:
        df = pd.read_csv(pos_file)
        pos = G.new_vp('vector<double>')
        ymin, ymax = df.y.min(), df.y.max()
        df['y'] = ymin + ymax - df.y

        for i, row in df.iterrows():
            node = row.route
            v = node_index[node]
            pos[v] = [row.x, row.y]
    elif layout_algo == 'sfdp':
        pos = sfdp_layout(G)
    elif layout_algo == 'fr':
        pos = fruchterman_reingold_layout(G, n_iter=2000)	
    else:
        pos = arf_layout(G, max_iter=0, d=5, a=5)

    if not pos_file:
        pos_file = 'cocite-coordination.csv'
        routes, xs, ys = [], [], []
        for v in range(len(node_index)):
            routes.append(node_names[v])
            x, y = pos[v]
            xs.append(x)
            ys.append(y)
        dat = pd.DataFrame({'route': routes, 'x': xs, 'y': ys})
        dat.to_csv(pos_file, index=False)
    return pos

def config_graph(G):
    # Properties of node_index: size, order, color
    vsz, vord, vc, fvc = G.new_vp('int'), G.new_vp('int'), G.new_vp('vector<float>'), G.new_vp('vector<float>')
    for i in range(len(node_index)):
        vsz[i], vord[i], vc[i] = 5, 0, np.array([128,128,128,256*0.3])/256
        fvc[i] = np.array([256,256,256,256*0.1])/256

    # Properties of routes: size, order, color
    esz, eord, ec = G.new_ep('int'), G.new_ep('int'), G.new_ep('vector<float>')

    for e in edges.values():
        esz[e],eord[e],ec[e] = 1, 0, np.array([153,216,201,256*0.3])/256 # light green
    return vsz, vord, vc, fvc, esz, eord, ec

node_names, node_index, edges, G = setup_cocite_net()
num_node, num_link = len(node_index), len(edges)

vsz, vord, vc, fvc, esz, eord, ec = config_graph(G)

def draw():
    output_file = 'cocitenet.png'

    highlighted = ['Jianxi Gao', 'Xiaozheng He', 'Lazaros Gallos', 'Nina Fefferman', 'Shlomo Havlin', 'Reuven Cohen', 'Efrat Blumenfeld-Lieberthal', 'Nimrod Serok']
    highcolor = [[228,26,28], [55,126,184],[77,175,74],[152,78,163],[255,127,0],[255,255,51],[166,86,40],[247,129,191]]
    highcolor = np.array(highcolor)/256

    for s, c in zip(highlighted, highcolor):
        np.append(c,1)
        u = node_index[s]
        vord[u], vc[u], fvc[u] = num_node, c, c

    #pos_file = 'cocite-coordination.csv'
    pos_file = ''

    pos = layout(G, node_names, node_index, pos_file=pos_file, layout_algo='sfdp')
    graph_draw(G, pos=pos, vertex_size=vsz, vertex_color=vc, vertex_fill_color=fvc, vorder=vord, 
               edge_pen_width=esz, edge_color=ec,eorder=eord, output=output_file,output_size=(300,300))

draw()