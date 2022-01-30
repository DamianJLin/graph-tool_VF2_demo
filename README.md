# graph-tool_VF2_demo
Demonstrating the VF2 algorithms implemented by graph-tool python package.

Usage
======
To run VF2 algorithm on all AG and all CG:

`python3 subgraph_isomorphism_demo.py`

The runtime will likely blow up on some of the larger circuit graphs (subgraphs). To run with a smaller subset of those:

`python3 subgraph_isomorphism_demo.py -c B131`.

Developed with Python 3.10.
