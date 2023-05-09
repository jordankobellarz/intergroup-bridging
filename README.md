# Intergroup Bridging Algorithm

The "Intergroup Bridging" Algorithm assesses a node's ability to serve as a bridge between different groups in a network. 

This algorithm was first employed to identify highly central nodes that could disseminate information between partisan groups in a polarized network, as described in the [main article](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-022-00357-3).


# Usage

The algorithm was created to work together with NetworkX library. 

The usage is extremelly simple:

```
from centralities.intergroup_bridging import intergroup_bridging_centrality
from centralities.intergroup_bridging_parallel import intergroup_bridging_centrality_parallel

results = intergroup_bridging_centrality(G_copy, attr='group')
```

Where `attr`refers to the attribute used to label nodes' groups. For example, in a polarized network, the `attr` could denote the nodes' political orientation. 


# Experiments

```
## Create and activate Conda env 
conda create --name intergroup-bridging python=3.11
conda activate intergroup-bridging

## Install required packages
conda install --file requirements.txt
# pip install -r requirements.txt
```

Execute the centralities_comparison.ipynb Jupyter Notebook to see a detailed comparison between classical Betweeness, Bridgeness and Intergroup Reaching algorithm values for toy networks. 


# How to cite

If you are using Intergroup Bridging Algorithm, please cite our [paper](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-022-00357-3):
```
@article{kobellarz2022reaching,
  title={Reaching the bubble may not be enough: news media role in online political polarization},
  author={Kobellarz, Jordan K and Bro{\'c}i{\'c}, Milo{\v{s}} and Graeml, Alexandre R and Silver, Daniel and Silva, Thiago H},
  journal={EPJ Data Science},
  volume={11},
  number={1},
  pages={47},
  year={2022},
  publisher={Springer Berlin Heidelberg}
}
```