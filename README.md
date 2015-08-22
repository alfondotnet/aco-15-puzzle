# 15 puzzle solver using Ant Colony Optimization and Pattern databases

Proof of concept on Ant Colony Optimization for solving a 15puzzle problem.

Although this problem is easily solved using [A* search](https://en.wikipedia.org/wiki/A*_search_algorithm), an example of how this problem could be solved using ACO was developed for a mathematics class, it was done in a couple of days, and I [struggled a bit with multiprocessing](https://github.com/alfonsoperez/aco-15-puzzle/blob/master/acoproblem.py) so at the end I got better results without it given the limited time I had for the task. (It's on my todo!)

It uses 6-6-3 [PDB (Pattern Database)](http://www.brian-borowski.com/software/puzzle/PatternDatabaseGenerator.java)  as optimal heuristic.
