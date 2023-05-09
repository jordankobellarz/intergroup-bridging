"""
Parallel implementation for Bridgeness centrality.
Reference: https://networkx.org/documentation/stable//auto_examples/advanced/plot_parallel_betweenness.html
"""

from centralities.bridgeness import bridgeness_centrality_subset

from multiprocessing import Pool
import itertools

__author__ = """Jordan Kobellarz (jordan@alunos.utfpr.edu.br)"""

__all__ = ['extract_bridgeness']


def chunks(l, n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        yield x


def bridgeness_centrality_parallel(G, processes=None):

    p = Pool(processes=processes)
    node_divisor = len(p._pool) * 4
    node_chunks = list(chunks(G.nodes(), int(G.order() / node_divisor)))
    num_chunks = len(node_chunks) 

    bt_sc = p.starmap(
        bridgeness_centrality_subset,
        zip(
            [G] * num_chunks,
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

