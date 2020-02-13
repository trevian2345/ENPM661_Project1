# ENPM 661 - Robot Planning - Project 1

### Description

This program uses Dijkstra's algorithm to solve an 8-puzzle --
a 3-slot-by-3-slot board of 8 sliding square tiles
numbered 1 through 8, with one open slot for sliding tile positions.
The user can provide an initial state and a goal state,
and the algorithm will output the minimum steps necessary to solve the puzzle.

--------------------------------------

### Execution

The program, solver.py, is run by executing the command `python -u solver.py`
from a terminal in the same directory.
If your python command is different, for example python3, adjust accordingly.
This script requires python 3.x to run.
The option `-u` allows output text to be written dynamically as the program is executed,
as opposed to being buffered and only output at the end.
This option is useful in Git Bash but not necessarily in other environments.

--------------------------------------

### Arguments

This script allows a few different optional arguments:
* `--puzzle`: allows the user to specify an input state in the form "0 1 2 3 4 5 6 7 8" which,
for this example, translates to the following format
(which also happens to be the default goal state):

        -------------
        |   | 1 | 2 |
        | 3 | 4 | 5 |
        | 6 | 7 | 8 |
        -------------

  Notice that a `0` corresponds to an empty space.
  When the puzzle argument is omitted, the solver generates a random solvable puzzle.

* `--goal`: allows the user to specify a goal state.  Has the same format as `--puzzle`.
The goal and puzzle values are checked to ensure that they create a valid puzzle.
For example, in the case that the start and goal states have opposite parities,
the puzzle would be unsolvable.
The user will receive feedback in the event of an invalid entry.
When the goal is omitted, it is assumed to be the default state previously described
("0 1 2 3 4 5 6 7 8").

Help with using the program can be found by running the command `python solver.py --help`.

Some examples of valid commands:

        python3 -u solver.py

        python3 -u solver.py --puzzle "3 1 6 7 4 8 5 0 2" --goal "0 2 3 1 4 5 6 7 8"

        python3 -u solver.py --puzzle "3 5 1 4 7 0 6 8 2"

--------------------------------------

### Output

While the solver is running, it will output its progress.
Once a solution has been found, the program outputs the runtime of the solution process.
The program also outputs an optimal sequence of actions to get
from the initial state to the goal state.
The files nodePath.txt, NodesInfo.txt, and Nodes.txt provide more details about
the data associated with finding the solution to the puzzle.
