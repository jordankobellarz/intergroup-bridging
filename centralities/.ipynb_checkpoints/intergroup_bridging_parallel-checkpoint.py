"""
Parallel implementation for Intergroup Bridging algorithm.
Reference: https://networkx.org/documentation/stable//auto_examples/advanced/plot_parallel_betweenness.html

Copyright (C) 2004-2011 by 
Jordan K. Kobellarz <jordan@alunos.utfpr.edu.br>
Miloš Broćić <milos.brocic@mail.utoronto.ca>
Alexandre R. Graeml <graeml@utfpr.edu.br>
Daniel Silver <dan.silver@utoronto.ca>
Thiago H. Silva <thiagoh@utfpr.edu.br>

All rights reserved.
BSD license.
"""

from centralities.intergroup_bridging import intergroup_bridging_centrality_subset

from multiprocessing import Pool
import itertools

__author__ = """Jordan Kobellarz (jordan@alunos.utfpr.edu.br)"""

__all__ = ['extract_intergroup_bridging']


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def intergroup_bridging_centrality_parallel(G, attr='group', processes=None):

    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks) 

    bt_sc = p.starmap(
        intergroup_bridging_centrality_subset,
        zip(
            [G] * num_chunks,
            [attr] * num_chunks,
            node_chunks,
            [list(G)] * num_chunks,
            [True] * num_chunks,
            [None] * num_chunks
        )
    )

    # Reduce the partial solutions
    bt_c = bt_sc[0]
    for bt in bt_sc[1:]:
        for n in bt:
            bt_c[n] += bt[n]
    return bt_c