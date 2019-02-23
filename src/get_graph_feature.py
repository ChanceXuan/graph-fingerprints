import os
import utils
import numpy as np
import networkx as nx

def count_thv(graph):
    thv = []
    for i in range(len(graph)):
        num_thv = 0
        nbs = list(graph.neighbors(i))
        for j in nbs:
            if graph.degree(j) > 1:
                num_thv = num_thv+1
        thv.append((i,num_thv))
    return thv

def cal_lcs(graph):
    lcs = []
    for i in range(len(graph)):
        fai = 0
        nbs1 = list(graph.neighbors(i))
        for j in nbs1:
            nbs2 = list(graph.neighbors(j))
            for k in nbs2:
                nbs3 = list(graph.neighbors(j))
                for v in nbs1:
                    if v in nbs3:
                        fai = fai + 1
        dv = graph.degree(i)
        if dv>1:
            cv = 2*fai/(dv-1)/dv
        else: cv = 0
        lcs.append((i,cv))
    return lcs

def cal_acn(graph, lcs):
    acn = []
    for i in range(len(graph)):
        nbs = list(graph.neighbors(i))
        sigma_cj = 0
        for j in nbs:
            cj = lcs[j][1]
            sigma_cj = sigma_cj +cj
        ncv = sigma_cj/len(nbs)
        acn.append((i,ncv))
    return acn

def count_tri(graph):
    tri = nx.triangles(G)
    num_tri = 0
    for i in tri:
        num_tri = num_tri + tri[i]
    return num_tri

def max_td(graph):
    total_degree = graph.degree
    max_temp = 0
    for i in total_degree:
        if i[1] > max_temp:
            max_temp = i[1]
    return max_temp

def cal_gcc(graph, num_tri):
    beta = 0
    for i in range(len(graph)):
        num_nbs = len(list(graph.neighbors(i)))
        beta = beta + num_nbs*(num_nbs-1)/2
    gc = 3*num_tri/beta
    return gc

dataset_name = 'citeseer'
sampled_dir=''
cache=True
dataset_filename = os.path.abspath(os.path.join('../data/{}'.format(dataset_name), sampled_dir, 'graph.edgelist'))
labels = os.path.abspath(os.path.join(os.path.dirname(dataset_filename), 'label.txt'))
save_path = os.path.abspath(os.path.join('../embeddings/{}'.format(dataset_name), sampled_dir, 'wme.embeddings'))
if (not cache) or (not os.path.exists(save_path)) or (os.path.getmtime(save_path) < os.path.getmtime(dataset_filename)):
    G = utils.load_graph(dataset_filename, label_name=None)
    do_full = (G.number_of_nodes()<10000)
    eigenvalues = 'full' if do_full else 'auto'
    # wne = netlsd.heat(G, timescales=np.logspace(-2, 2, 10), eigenvalues=eigenvalues)
    
    centrality = nx.eigenvector_centrality(G)
    print('%s %0.2f'%(node,centrality[node]) for node in centrality)

    pr = nx.pagerank(G, alpha=0.9)
    print('%s %0.2f'%(node,pr[node]) for node in pr)

    print('\n======Degree======')
    total_degree = G.degree
    print(list(total_degree))

    # Two-Hop Away Neighbours
    print('\n======Two-Hop Away Neighbours======')
    two_hop = count_thv(G)
    print(two_hop)

    # Local Clustering Score
    print('\n======Local Clustering Score======')
    local_clustering_score = cal_lcs(G)
    print(local_clustering_score)

    # Average Clustering of Neighbourhood
    print('\n======Average Clustering of Neighbourhood======')
    average_clustering_of_neighbors = cal_acn(G, local_clustering_score)
    print(average_clustering_of_neighbors)

    graph_order = nx.Graph.order(G)
    print('graph order =', graph_order)

    num_edges = nx.number_of_edges(G)
    print('number of edges =', num_edges)

    num_triangles = count_tri(G)
    print('number of triangles =', num_triangles)

    global_clustering_coefficient = cal_gcc(G, num_triangles)
    print('global clustering coefficient =', global_clustering_coefficient)

    max_total_degree = max_td(G)
    print('max total degree =', max_total_degree)

    num_components = nx.number_connected_components(G)
    print('number of components =', num_components)

    # with utils.write_with_create(save_path) as f:
        # print(" ".join(map(str, wne)), file=f)