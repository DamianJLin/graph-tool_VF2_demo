from pathlib import Path
import networkx as nx

# Generates .graphml files for graphs of the list of architectures in [Li et al., 2021]. (TODO: Add grid architecture).
# Following graph-generation code retrieved from https://github.com/ebony72/FiDLS/blob/master/ag.py

AG_dict = {}


# IBM Q Tokyo
ag_tokyo = nx.Graph()
ag_tokyo.add_nodes_from(list(range(20)))

for i in range(0, 4):
    ag_tokyo.add_edge(i, i + 1)
    ag_tokyo.add_edge(i + 1, i)

for i in range(5, 9):
    ag_tokyo.add_edge(i, i + 1)
    ag_tokyo.add_edge(i + 1, i)

for i in range(10, 14):
    ag_tokyo.add_edge(i, i + 1)
    ag_tokyo.add_edge(i + 1, i)

for i in range(15, 19):
    ag_tokyo.add_edge(i, i + 1)
    ag_tokyo.add_edge(i + 1, i)

for i in range(0, 15):
    ag_tokyo.add_edge(i, i + 5)
    ag_tokyo.add_edge(i + 5, i)

for i in [1, 3, 5, 7, 11, 13]:
    ag_tokyo.add_edge(i, i + 6)
    ag_tokyo.add_edge(i + 6, i)

for i in [2, 4, 6, 8, 12, 14]:
    ag_tokyo.add_edge(i, i + 4)
    ag_tokyo.add_edge(i + 4, i)

AG_dict['AG_Tokyo'] = ag_tokyo


# IBM Rochester
ag_rochester = nx.Graph()
ag_rochester.add_nodes_from(list(range(0, 53)))

ranges = list(range(4)) + list(range(7, 15)) + list(range(19, 27)) + list(range(30, 38)) + list(range(42, 50))
for i in ranges:
    ag_rochester.add_edge(i, i + 1)

E = [(0, 5), (5, 9), (4, 6), (6, 13), (7, 16), (16, 19), (11, 17), (17, 23), (15, 18), (18, 27), (21, 28), (28, 32),
     (25, 29), (29, 36), (30, 39), (39, 42), (34, 40), (40, 46), (38, 41), (41, 50), (44, 51), (48, 52)]
ag_rochester.add_edges_from(E)

AG_dict['AG_Rochester'] = ag_rochester


# Google Sycamore
ag_sycamore = nx.Graph()
ag_sycamore.add_nodes_from(list(range(0, 54)))

ranges = list(range(6, 12)) + list(range(18, 24)) + list(range(30, 36)) + list(range(42, 48))
for i in ranges:
    for j in ag_sycamore.nodes():
        if j in ranges:
            continue
        if i - j in [5, 6] or j - i in [6, 7]:
            ag_sycamore.add_edge(i, j)

ag_sycamore.remove_node(3)
assert 3 not in ag_sycamore.nodes()

mapping = dict()
for n in ag_sycamore.nodes():
    if n < 3:
        mapping[n] = n
    else:
        mapping[n] = n - 1

nx.relabel_nodes(ag_sycamore, mapping, copy=False)

AG_dict['AG_Sycamore'] = ag_sycamore


# Grid m x n
def ag_grid(m, n):
    graph = nx.Graph()
    graph.add_nodes_from(list(range(0,m*n-1)))
    for x in range(0, m):
        for y in range(0 , n):
            if x < m - 1:
                graph.add_edge(y * m + x, y * m + x + 1)
            if y < n - 1:
                graph.add_edge(y * m + x, (y + 1) * m + x)
    return graph


AG_dict['AG_Grid5x5'] = ag_grid(5, 5)
AG_dict['AG_Grid9x9'] = ag_grid(9, 9)
AG_dict['AG_Grid19x19'] = ag_grid(19, 19)


# Write to GraphML files

write_path = Path(__file__).resolve().parent / 'architecture_graphs'

# Warn user we are about to overwrite any files in the above directory.
if input(f'(Over)write files in the directory {write_path}? (y or n)\n') in {'y', 'Y'}:
    write_path.mkdir(exist_ok=True)

    for filename, graph in AG_dict.items():
        nx.write_graphml(
                graph, 
                write_path / (filename + '.graphml')
            )
