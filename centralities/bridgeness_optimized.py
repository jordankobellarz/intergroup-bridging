"""
Bridgeness centrality measures.
"""
#    Copyright (C) 2004-2011 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Bridgeness extensions Matteo Morini <matteo.morini@ens-lyon.fr>
#    All rights reserved.
#    BSD license.
import heapq
import networkx as nx
import random

from networkx.algorithms.centrality.betweenness import _single_source_dijkstra_path_basic, _single_source_shortest_path_basic, _rescale, _rescale_e

__author__ = """Aric Hagberg (hagberg@lanl.gov), Matteo Morini (matteo.morini@ens-lyon.fr)"""

__all__ = ['bridgeness_centrality', 'bridgeness_centrality_subset']

def bridgeness_centrality(G, k=None, normalized=True, weight=None, seed=None):
    
    #SP = dict(nx.shortest_path_length(G)) # precompute shortest paths between all nodes
    bridgeness=dict.fromkeys(G,0.0) # b[v]=0 for v in G

    if k is None:
        nodes = G
    else:
        random.seed(seed)
        nodes = random.sample(G.nodes(), k)
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S,P,sigma=_single_source_shortest_path_basic(G,s)
        else:  # use Dijkstra's algorithm
            S,P,sigma=_single_source_dijkstra_path_basic(G,s,weight)
        # accumulation
        bridgeness=_accumulate_basic(G,bridgeness,S,P,sigma,s)
    # rescaling
    bridgeness=_rescale(bridgeness, len(G),
                         normalized=normalized,
                         directed=G.is_directed(),
                         k=k)
    return bridgeness

def _accumulate_basic(G, bridgeness, S, P, sigma, s):     
    
    delta=dict.fromkeys(S,0)
    delta_bri=dict.fromkeys(S,0)
    while S:
        w=S.pop()
        coeff=(1.0+delta[w])/sigma[w]
        coeff_bri=(delta[w])/sigma[w] #1.0 removed
        
        for v in P[w]:            
            delta[v] += sigma[v]*coeff            
            delta_bri[v] += sigma[v]*coeff_bri
            
        if w != s and not w in G.neighbors(s):
            bridgeness[w] += delta_bri[w]
    
    return bridgeness


def bridgeness_centrality_subset(G, sources, targets, normalized=False, weight=None):
   
    bridgeness = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    
    for s in sources:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        bridgeness = _accumulate_subset(G, bridgeness, S, P, sigma, s, targets)
    # rescaling
    bridgeness=_rescale(bridgeness, len(G),
                         normalized=normalized,
                         directed=G.is_directed())
    return bridgeness

def _accumulate_subset(G, bridgeness, S, P, sigma, s, targets):

    delta=dict.fromkeys(S,0)
    delta_bri=dict.fromkeys(S,0)
    target_set = set(targets) - {s}
    while S:
        w = S.pop()
        if w in target_set:
            coeff=(1.0+delta[w])/sigma[w]
            coeff_bri=(delta[w])/sigma[w] #1.0 removed
        else:
            coeff=delta[w]/sigma[w]
            coeff_bri=delta[w]/sigma[w]
            
        for v in P[w]:
            delta[v] += sigma[v]*coeff            
            delta_bri[v] += sigma[v]*coeff_bri
        
        if w != s and not w in G.neighbors(s):
            bridgeness[w] += delta_bri[w]
            
    return bridgeness