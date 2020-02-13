import random
import time
import sys
from datetime import datetime
import io
import argparse


class solver:
    def __init__(self, goal, puzzle=None):
        self.openList = []
        self.closeList = []
        self.actionList = []
        self.initial_state = []
        self.actions = [[(i >> 1) * (1 if i & 1 else -1), (1 if (i & 1) else -1) if not i >> 1 else 0] for i in range(4)]
        self.max_states = 9*8*7*6*5*4*3
        self.nodePath = "nodePath.txt"
        self.nodeInfo = "NodesInfo.txt"
        self.nodesExplored = "Nodes.txt"

        # Initialize the solver with a user-specified goal if it is valid.  Print an error message and exit otherwise.
        self.goal_state = self.convert_puzzle(goal, "goal puzzle")

        # Randomize the puzzle if it is not specified by the user.
        if puzzle is None:
            self.random_init()
            while self.is_even_parity(self.initial_state) != self.is_even_parity(self.int_to_state(self.goal_state)):
                self.random_init()

        # Initialize the solver with a user-specified puzzle if it is valid.  Print an error message and exit otherwise.
        else:
            self.initial_state = self.int_to_state(self.convert_puzzle(puzzle, "initial puzzle"))



    def convert_puzzle(self, puzzle, which_puzzle):
        puzzle_args = []
        try:
            puzzle_args = [int(i) for i in str(puzzle).split()]
        except ValueError:
            self.print_error(which_puzzle, "noninteger value supplied")
        if len(puzzle_args) != 9:
            self.print_error(which_puzzle, "wrong number of values")
        supplied_values = []
        for i in puzzle_args:
            if i < 0 or i > 8:
                self.print_error(which_puzzle, "%d is outside of range 0 to 8" % i)
            if i in supplied_values:
                self.print_error(which_puzzle, "multiple copies of %d" % i)
            supplied_values.append(i)

        return sum([(puzzle_args[i] << (8 - i)*4) for i in range(9)])

    @staticmethod
    def print_error(which_puzzle, error):
        sys.stdout.write("\nERROR:  Incorrect format for the %s:  %s." % (which_puzzle, error))
        sys.stdout.write("\nEnsure that the following are true for the %s." % which_puzzle)
        sys.stdout.write("\n   1. You supplied exactly 9 values.")
        sys.stdout.write("\n   2. You supplied only integers from 0 to 8.")
        sys.stdout.write("\n   3. Each integer you supplied is unique.\n")
        exit(0)

    @staticmethod
    def print_state(state):
        print("-------------\n%s\n-------------" % "\n".join("|%s|" % ("|".join(" %s " % (str(col) if col != 0 else " ") for col in row)) for row in state))

    def random_init(self):
        self.initial_state = []
        chosen_numbers = []
        for i in range(3):
            nextLine = []
            for j in range(3):
                num = random.randrange(0, 9)
                while num in chosen_numbers:
                    num = random.randrange(0, 9)
                chosen_numbers.append(num)
                nextLine.append(num)
            self.initial_state.append(nextLine)

    @staticmethod
    def state_to_int(state):
        state_as_int = 0
        for i in range(3):
            for j in range(3):
                state_as_int = (state_as_int << 4) | state[i][j]
        return state_as_int

    @staticmethod
    def int_to_state(num: int):
        int_as_state = []
        for i in range(3):
            nextLine = []
            for j in range(3):
                nextLine.append((num >> (4*((2-i)*3 + (2-j)))) & 0xF)
            int_as_state.append(nextLine)
        return int_as_state

    @staticmethod
    def findSpace(state):
        y = next(n for n in range(3) if 0 in state[n])
        x = next(n for n in range(3) if state[y][n] == 0)
        return y, x

    def move(self, state, action: list, backwards=False):
        try:
            y, x = self.findSpace(state)
            new_y: int = action[0]*(-1 if backwards else 1) + y
            new_x: int = action[1]*(-1 if backwards else 1) + x
            new_state = [[col for col in row] for row in state]
            new_state[y][x] = state[new_y][new_x]
            new_state[new_y][new_x] = 0
            return new_state
        except IndexError:
            return None

    @staticmethod
    def is_even_parity(state):
        inversions = 0
        for i in range(3):
            for j in range(3):
                for m in range(3):
                    for n in range(3):
                        if m > i or (m == i and n > j):
                            if state[m][n] < state[i][j] and state[m][n] != 0:
                                inversions += 1
        return False if inversions % 2 else True

    def solve(self):
        sys.stdout.write("\nInitial state:\n")
        self.print_state(self.initial_state)
        sys.stdout.write("\nGoal state:\n")
        self.print_state(self.int_to_state(self.goal_state))
        if not (self.is_even_parity(self.initial_state) == self.is_even_parity(self.int_to_state(self.goal_state))):
            sys.stdout.write("ERROR: This is NOT solvable!\n")
            exit(1)

        time.sleep(0.75)
        start_time = datetime.today()
        self.openList = [(self.state_to_int(self.initial_state), 0, -1)]

        # Expand cells while there are cells on the open list
        while len(self.openList) > 0:
            # Search for open state with least cost
            minimum = -1
            index = -1
            for i in range(len(self.openList)):
                state, cost, previous_action = self.openList[i]
                if cost < minimum or minimum < 0:
                    index = i
                    minimum = cost

            # Expand an open cell
            current_state = self.int_to_state(self.openList[index][0])
            sys.stdout.write("\rProgress: %06d out of %d possible states" % (len(self.closeList), self.max_states))
            sys.stdout.write(" -- %.2f %%" % (100 * len(self.closeList) / self.max_states))
            space_y, space_x = self.findSpace(current_state)
            for action_index, action in enumerate(self.actions):
                new_y = space_y + action[0]
                new_x = space_x + action[1]
                new_cost = self.openList[index][1] + 1
                if 0 <= new_y <= 2 and 0 <= new_x <= 2:
                    new_state = self.move(current_state, action)
                    new_state_as_int = self.state_to_int(new_state)
                    if new_state_as_int not in self.closeList:
                        if new_state_as_int not in [self.openList[i][0] for i in range(len(self.openList))]:
                            self.openList.append((new_state_as_int, new_cost, action_index))
            self.closeList.append(self.openList[index][0])
            self.actionList.append(self.openList[index][2])

            # Check for the goal state
            if self.openList[index][0] == self.goal_state:
                self.openList.clear()
            else:
                self.openList.pop(index)

        end_time = datetime.today()
        duration = end_time - start_time
        print("\nSolution found!" if self.closeList[len(self.closeList) - 1] == self.goal_state else "\nFailure...")
        sys.stdout.write("\nStart time:  %s\nEnd time:  %s" % (start_time, end_time))
        sys.stdout.write("\nRuntime:  ")
        sys.stdout.write(("%d hr, " % (duration.seconds // 3600)) \
                             if duration.seconds >= 3600 else "")
        sys.stdout.write(("%d min, " % ((duration.seconds // 60) % 3600)) \
                             if (duration.seconds // 60) % 3600 >= 1 else "")
        sys.stdout.write("%.3f sec" % ((duration.seconds % 60) + (duration.microseconds / 1000000.0)))

    def displaySolution(self):
        next_action_index = next(i for i in range(len(self.closeList)) if self.closeList[i] == self.goal_state)
        next_state = self.int_to_state(self.goal_state)
        state_list = [self.int_to_state(self.goal_state)]
        while self.actionList[next_action_index] != -1:
            next_action = self.actions[self.actionList[next_action_index]]
            next_state = self.move(next_state, next_action, backwards=True)
            state_list.append(next_state)
            next_action_index = next(i for i in range(len(self.closeList)) if self.closeList[i] == self.state_to_int(next_state))
        state_list.reverse()
        sys.stdout.write("\n\nOptimal solution is as follows (%d total moves):\n" % (len(state_list) - 1))
        is_open = False
        nodePath = None
        nodeInfo = None
        nodesExplored = None
        try:
            nodePath = io.open(self.nodePath, mode="wt")
            nodeInfo = io.open(self.nodeInfo, mode="wt")
            nodesExplored = io.open(self.nodesExplored, mode="wt")
            is_open = True
        except (FileNotFoundError, FileExistsError):
            sys.stdout.write("Unable to open text file for writing.")
        for i in range(len(state_list)):
            if i > 0:
                sys.stdout.write("\nStep %d:\n" % i)
            if is_open:
                nodePath.write("%s\n" % " ".join(" ".join("%d" % state_list[i][j][k] for j in range(3)) for k in range(3)))
            self.print_state(state_list[i])

        # Append node parent information to NodesInfo in the form of <node_index, parent_index>
        sys.stdout.write("\nWriting to output files %s, %s, and %s..." % (self.nodeInfo, self.nodePath, self.nodesExplored))
        for i in range(len(self.closeList)):
            nodesExplored.write("%s\n" % " ".join(" ".join("%d" % self.int_to_state(self.closeList[i])[j][k] for j in range(3)) for k in range(3)))
            # if i == 0:
            #     nodeInfo.write("1 0\n")
            # else:
            #     nodeInfo.write("%d %d\n" % (i + 1,
            #         next(j + 1 for j in range(len(self.closeList)) if self.state_to_int(self.move(self.int_to_state(self.closeList[i]), self.actions[self.actionList[i]], backwards=True)) == self.closeList[j])))

        # Close files
        nodePath.close()
        nodeInfo.close()
        nodesExplored.close()
        sys.stdout.write("\nDone!\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Solves an 8-puzzle.")
    parser.add_argument('--puzzle', type=str,
                        help="Solve the provided puzzle.  Value has the format 'N0 N1 N2 N3 N4 N5 " \
                                         "N6 N7 N8' where Nx are unique integers from 0 to 8, and 0 denotes the " \
                                         "blank space. Puzzle is randomly generated by default.")
    parser.add_argument('--goal', type=str, default="0 1 2 3 4 5 6 7 8",
                        help="Set the goal to the provided puzzle string.  Has the same format as the " \
                                         "--puzzle argument.  Default value: %(default)s.")
    parser.add_argument('--animate', action="store_true",
                        help="Display an animation of the sliding puzzle being solved. Default value: %(default)s.")
    v = argparse.Namespace()
    args = parser.parse_args(namespace=v)
    S = solver(v.goal, v.puzzle)
    S.solve()
    time.sleep(0.5)
    S.displaySolution()