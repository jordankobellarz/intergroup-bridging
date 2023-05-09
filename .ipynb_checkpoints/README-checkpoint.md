# Intergroup Bridging Algorithm

The "Intergroup Bridging" Algorithm assesses a node's ability to serve as a bridge between different groups in a network. 

This algorithm was first employed to identify highly central nodes that could disseminate information between partisan groups in a polarized network, as described in the [main article](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-022-00357-3).


## ✌ Usage

The algorithm was created to work together with NetworkX library, so the usage is extremelly simple:

```
from centralities.intergroup_bridging import intergroup_bridging_centrality

results = intergroup_bridging_centrality(G_copy, attr='group')
```

Where `attr`refers to the attribute you have chosen to label nodes' groups. 

For example, in a polarized network, the `attr` could denote the nodes' political orientation. 

### ⚡ Parallelized version

We also implemented a faster version using parallel computing for large graphs: 

```
from centralities.intergroup_bridging_parallel import intergroup_bridging_centrality_parallel

results = intergroup_bridging_centrality_parallel(G_copy, attr='group', processes=8) 
```

This version partitionate the network in `processes` groups and combine results after Intergroup Bridging calculation.


## 🧪 Experiments

We created some experiments to compare Betweeness, Bridgeness and Intergroup Bridging algorithms results. 

These experiments are documented in the `centralities_comparison.ipynb` Jupyter Notebook. 

Just run the code bellow in your terminal to create a Conda enviroment and execute the notebook to see the results and/or test with your own networks. 

```
## Create and activate Conda env 
conda create --name intergroup-bridging python=3.11
conda activate intergroup-bridging

## Install required packages
conda install --file requirements.txt

## Run Jupyter
jupyter notebook

## Finaly, execute centralities_comparison.ipynb
```


## ✍️ How to cite

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

## Reach us

jordan[at]alunos.utpr.edu.br

Change `[at]` to `@`