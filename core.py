# base libraries
import pandas as pd
import numpy as np
import networkx as nx

# centralities
from centralities.bridgeness import bridgeness_centrality
from centralities.bridgeness_parallel import bridgeness_centrality_parallel
from centralities.intergroup_bridging import intergroup_bridging_centrality
from centralities.intergroup_bridging_parallel import intergroup_bridging_centrality_parallel


def filter_nodes(G, key, value):
    return G.subgraph([node for node, attr in G.nodes.items() if attr[key] is value])


def filter_edges(G, key, value):
    return G.edge_subgraph([edge for edge, attr in G.edges.items() if attr[key] is value])


def f_percent(x):
    return str(x) + '%'


def graph_to_dataframe(G):
    return pd.DataFrame([G.nodes[node] for node in G.nodes])


def set_node_attribute(G, attribute, values):
    for i, node in enumerate(G.nodes):
        G.nodes[node][attribute] = values[i]


def min_max_norm(values):
    values = np.array(values)
    return (values-np.min(values))/(np.max(values)-np.min(values))


def extract_degrees(G):

    print('Calculating degree centralities...')
    degrees = [degree for node, degree in G.degree(weight='weight')]
    set_node_attribute(G, 'degree', degrees)

    if nx.is_directed(G):
        in_degrees = [in_degree for node, in_degree in G.in_degree(weight='weight')]
        set_node_attribute(G, 'in_degree', in_degrees)
        set_node_attribute(G, 'in_degree_%', [in_degrees[i] / degrees[i] if degrees[i] > 0 else 0 for i in range(len(in_degrees))])

        out_degrees = [out_degree for node, out_degree in G.out_degree(weight='weight')]
        set_node_attribute(G, 'out_degree', out_degrees)
        set_node_attribute(G, 'out_degree_%', [out_degrees[i] / degrees[i] if degrees[i] > 0 else 0 for i in range(len(out_degrees))])


def extract_betweenness(G, weight='weight'):

    print('Calculating Betweeness centrality...')

    G_copy = G.to_undirected()

    results = nx.centrality.betweenness_centrality(G_copy, weight=weight)
    results = min_max_norm(list(results.values()))

    set_node_attribute(G, 'betweenness', results)


def extract_bridgeness(G, processes=None):

    print('Calculating Bridgeness centrality...')

    G_copy = G.to_undirected()

    results = bridgeness_centrality(G_copy)
    results = min_max_norm(list(results.values()))

    set_node_attribute(G, 'bridgeness', results)


def extract_bridgeness_parallel(G, processes=None):

    print('Calculating Bridgeness (parallel) centrality...')

    G_copy = G.to_undirected()

    results = bridgeness_centrality_parallel(G_copy, processes)
    results = min_max_norm(list(results.values()))

    set_node_attribute(G, 'bridgeness', results)


def extract_intergroup_bridging(G, attr="group"):

    print('Calculating Intergroup Reaching centrality...')

    G_copy = G.to_undirected()

    results = intergroup_bridging_centrality(G_copy, attr)
    results = min_max_norm(list(results.values()))

    set_node_attribute(G, 'intergroup_bridging', results)


def extract_intergroup_bridging_parallel(G, attr="group", processes=None):

    print('Calculating Intergroup Bridging (parallel) centrality...')

    G_copy = G.to_undirected()

    results = intergroup_bridging_centrality_parallel(G_copy, attr, processes)
    results = min_max_norm(list(results.values()))

    set_node_attribute(G, 'intergroup_bridging', results)