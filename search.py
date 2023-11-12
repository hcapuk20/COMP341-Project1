# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    """
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = []  # needs to be iterable in order to check items (can not do it in util data structures)
    dfs_stack = util.Stack()  # main dfs stack, elements will hold current position, and path it took to get there.
    dfs_stack.push((problem.getStartState(), []))

    while not dfs_stack.isEmpty():
        current_position, current_path = dfs_stack.pop()
        visited.append(current_position)
        if problem.isGoalState(current_position):
            return current_path

        for successor in problem.getSuccessors(current_position):
            if successor[0] not in visited:
                dfs_stack.push((successor[0], current_path + [successor[1]]))

    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = []  # needs to be iterable in order to check items (can not do it in util data structures)
    bfs_queue = util.Queue()  # main bfs queue, elements will hold current position, and path it took to get there.
    bfs_queue.push((problem.getStartState(), []))
    while not bfs_queue.isEmpty():
        current_position, current_path = bfs_queue.pop()
        if problem.isGoalState(current_position):
            return current_path

        if current_position not in visited:
            visited.append(current_position)
            for successor in problem.getSuccessors(current_position):
                # check after the "and" clause is for q5 where successor holds also the corner states.
                if successor[0] not in visited and successor[0] not in (state[0] for state in bfs_queue.list):
                    bfs_queue.push((successor[0], current_path + [successor[1]]))

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = []  # needs to be iterable in order to check items (can not do it in util data structures)
    ucs_pqueue = util.PriorityQueue()  # main pqueue to hold frontier
    ucs_pqueue.push((problem.getStartState(), []), 0)  # pushing the starting point to prio queue with 0 cost

    while not ucs_pqueue.isEmpty():
        current_position, current_path = ucs_pqueue.pop()  # least cost operation at the time
        if problem.isGoalState(current_position):
            return current_path

        if current_position not in visited:
            visited.append(current_position)
            for successor in problem.getSuccessors(current_position):
                if successor[0] not in visited:
                    new_path = current_path + [successor[1]]
                    # adding the unvisited node to prio queue with its cost.
                    ucs_pqueue.push((successor[0], new_path),problem.getCostOfActions(new_path))

    return []
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    visited = []
    aStar_pqueue = util.PriorityQueue()
    aStar_pqueue.push((problem.getStartState(), []), 0.0)

    while not aStar_pqueue.isEmpty():
        current_position, current_path = aStar_pqueue.pop()
        if problem.isGoalState(current_position):
            return current_path

        if current_position not in visited:
            visited.append(current_position)
            for successor in problem.getSuccessors(current_position):
                if successor[0] not in visited and successor[0] not in (state[0] for state in aStar_pqueue.heap):
                    new_path = current_path + [successor[1]]
                    # f(s) = g(s) + h(s)   g(s) = cost from start to the next node
                    calculated_cost = float(problem.getCostOfActions(current_path)) + successor[2] + float(heuristic(successor[0], problem))
                    aStar_pqueue.push((successor[0], new_path),calculated_cost)

    return []
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
