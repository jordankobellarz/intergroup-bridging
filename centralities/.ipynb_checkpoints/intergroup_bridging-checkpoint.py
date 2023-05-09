"""
Intergroup Bridging algorithm, adapted from Bridgeness algorithm, which extends 
Brandes' faster algorithm for betweenness centrality.

Copyright (C) 2004-2011 by 
Aric Hagberg <hagberg@lanl.gov>
Dan Schult <dschult@colgate.edu>
Pieter Swart <swart@lanl.gov>

Bridgeness extensions by
Matteo Morini <matteo.morini@ens-lyon.fr>

Copyright (C) 2023 by 
Intergroup Bridging extensions by 
Jordan K. Kobellarz <jordan@alunos.utfpr.edu.br>
Miloš Broćić <milos.brocic@mail.utoronto.ca>
Alexandre R. Graeml <graeml@utfpr.edu.br>
Daniel Silver <dan.silver@utoronto.ca>
Thiago H. Silva <thiagoh@utfpr.edu.br>

All rights reserved.
MIT license.
"""


import random

from networkx.algorithms.centrality.betweenness import _single_source_dijkstra_path_basic, _single_source_shortest_path_basic, _rescale

__author__ = """Jordan K. Kobellarz (jordan@alunos.utfpr.edu.br)"""

__all__ = ['intergroup_bridging_centrality', 'intergroup_bridging_centrality_subset']


def intergroup_bridging_centrality(G, attr='group', k=None, normalized=True, weight=None, seed=None):

    intergroup_bridging = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G

    if k is None:
        nodes = G
    else:
        random.seed(seed)
        nodes = random.sample(G.nodes(), k)
    for s in nodes:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, D = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, D = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        intergroup_bridging =_accumulate_basic(G, intergroup_bridging, S, P, sigma, s, attr)
    # rescaling
    intergroup_bridging =_rescale(intergroup_bridging, len(G),
                         normalized=normalized,
                         directed=G.is_directed(),
                         k=k)
    return intergroup_bridging


def _accumulate_basic(G, intergroup_bridging, S, P, sigma, s, attr='group'):

    delta = dict.fromkeys(S,0)
    delta_bri = dict.fromkeys(S,0)
    while S:
        w = S.pop()
        coeff = (1.0+delta[w])/sigma[w]
        coeff_bri = (delta[w])/sigma[w]  # 1.0 removed

        for v in P[w]:
            delta[v] += sigma[v]*coeff
            delta_bri[v] += sigma[v]*coeff_bri

        if w != s and (w not in G.neighbors(s) or w in G.neighbors(s) and G.nodes[w][attr] != G.nodes[s][attr]):
            intergroup_bridging[w] += delta_bri[w]

    return intergroup_bridging


def intergroup_bridging_centrality_subset(G, sources, targets, normalized=False, weight=None):

    intergroup_bridging = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G

    for s in sources:
        # single source shortest paths
        if weight is None:  # use BFS
            S, P, sigma, D = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma, D = _single_source_dijkstra_path_basic(G, s, weight)
        # accumulation
        intergroup_bridging = _accumulate_subset(G, intergroup_bridging, S, P, sigma, s, targets, attr)
    # rescaling
    intergroup_bridging = rescale(intergroup_bridging, len(G),
                         normalized=normalized,
                         directed=G.is_directed())
    return intergroup_bridging


def _accumulate_subset(G, intergroup_bridging, S, P, sigma, s, targets, attr='group'):

    delta = dict.fromkeys(S,0)
    delta_bri = dict.fromkeys(S,0)
    target_set = set(targets) - {s}
    while S:
        w = S.pop()
        if w in target_set:
            coeff = (1.0+delta[w])/sigma[w]
            coeff_bri = (delta[w])/sigma[w]  # 1.0 removed
        else:
            coeff = delta[w]/sigma[w]
            coeff_bri = delta[w]/sigma[w]

        for v in P[w]:
            delta[v] += sigma[v]*coeff
            delta_bri[v] += sigma[v]*coeff_bri

        if w != s and (w not in G.neighbors(s) or w in G.neighbors(s) and G.nodes[w][attr] != G.nodes[s][attr]):
            intergroup_bridging[w] += delta_bri[w]

    return intergroup_bridging