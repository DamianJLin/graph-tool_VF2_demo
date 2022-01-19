from pathlib import Path
import sys
import numpy as np
import graph_tool.all as gt


data_dir = Path(__file__).resolve().parent / 'data'
ag_dir = Path(__file__).resolve().parent / 'architecture_graphs'

match sys.argv[1:]:

    case []:
        cg_dir = Path(__file__).resolve().parent / 'circuit_graphs'

    case ['-c', cg_subdir]:
        cg_dir = Path(__file__).resolve().parent / 'circuit_graphs' / cg_subdir
        if not cg_dir.is_dir():
            raise ValueError(f'{cg_dir} is not a valid directory.')

    case _:
        raise ValueError('Arguments invalid.')

AG_FILEPATHS_ORDER = {
    'AG_Tokyo.graphml': 0,
    'AG_Sycamore.graphml': 1,
    'AG_Rochester.graphml': 1,
    'AG_Grid5x5.graphml': 2,
    'AG_Grid9x9.graphml': 3,
    'AG_Grid19x19.graphml': 4
        }

ag_filepaths = sorted(
    list(ag_dir.rglob('*.graphml')), 
    key=lambda path: AG_FILEPATHS_ORDER[path.name]
)
cg_filepaths = list(cg_dir.rglob('*.graphml'))

# Create data dir, empty data_dir of previous files for consistency.
if data_dir.exists():
    for f in data_dir.iterdir():
        assert not f.is_dir()
        f.unlink()
else:
    data_dir.mkdir()

success_array = np.empty(
    (len(ag_filepaths), len(cg_filepaths)),
    dtype=bool
)
num_combinations = np.size(success_array)

# Recursively iterate through these directories looking for .graphml files.
# ag_ind, cg_ind are indices for the relevant circuit and architecture graphs.
for ag_ind, ag_path in enumerate(ag_filepaths):
    ag = gt.load_graph(str(ag_path))
    ag.set_directed(False)

    for cg_ind, cg_path in enumerate(cg_filepaths):
        cg = gt.load_graph(str(cg_path))
        cg.set_directed(False)

        # Calculate the index of the current iteration.
        i = ag_ind * len(cg_filepaths) + cg_ind

        search_str = f'[{i} / {num_combinations}] Graph: {ag_path.stem}, Subgraph: {cg_path.stem}, searching for ' \
                     f'isomorphisms... '
        print(search_str, end='\n')

        isom_gen = gt.subgraph_isomorphism(
            cg,
            ag,
            generator=True
        )

        # Take from generator if not exhausted.
        _exhausted = object()
        isom_option = next(isom_gen, _exhausted)

        if isom_option is not _exhausted:

            success_array[ag_ind][cg_ind] = True
            data_filename = data_dir / f'map_{cg_path.stem}_into_{ag_path.stem}.txt'
            print(f'Mapping found, writing to {data_filename.relative_to(data_filename.parents[1])}.')

            with open(data_filename, 'w') as file:
                file.write('Subgraph --> Graph\n')
                for v in cg.vertices():
                    file.write(f'{str(int(v))} --> {str(isom_option[v])}\n') 

        else:

            success_array[ag_ind][cg_ind] = False

print(f'Successfully found mappings for {np.sum(success_array)} / {num_combinations} combinations.')
