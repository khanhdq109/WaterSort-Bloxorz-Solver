# WaterSort & Bloxorz Solver
The solvers for Bloxorz and Water Sort problems using DFS, BFS, A* and Genetic Algorithm

## Project structure
* [Stage](./Stage) 		          : the folder contains input maps for Bloxorz problem
* [Output](./Output) 		        : the folder contains outputs for Bloxorz problem
* [bloxorz.py](./bloxorz.py) 		: source code for Bloxorz Solver
* [map](./map) 		              : the folder contains input maps for Water Sort problem
* [output](./output) 		        : the folder contains outputs for Water Sort problem
* [WaterSortSolver.py](./[WaterSortSolver.py) 		: source code for Water Sort Solver

## Execute
### Bloxorz
Running the program with command line syntax:
```
python bloxorz.py <stage> <algorithm>
```
Example: 
```
python bloxorz.py 1 BFS
```
```
python bloxorz.py 3 genetic
```
The outputs will be created in "Output" folder

### Water Sort
Running this command line to install all necessary libraries
```
pip install -r requirements.txt
```
Then running this to running the program
```
python WaterSortSolver.py
```
The outputs will be created in "output" folder
