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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # print problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())

    branches = util.Stack() # tine evidenta starilor de explorat
    branches.push(problem.getStartState())  # punem start state in stiva
    visited = []
    path = [] # calea finala
    pathToCurr = util.Stack() # stiva pt cai intermediare
    currState = branches.pop()

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for child, direction, cost in successors:
                branches.push(child) # adaugam succesorul in stiva
                tempPath = path + [direction] # cale temp pt a ajunge de la copii la calea actuala
                pathToCurr.push(tempPath)  # salvam calea temp in stiva
        currState = branches.pop() # exploram urmatoarea stare
        path = pathToCurr.pop() # extragem calea asociata cu starea curenta din stiva
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    branches = util.Queue() # tine evidenta starilor de explorat
    branches.push(problem.getStartState())
    visited = []
    path = []
    pathToCurr = util.Queue() # coada pt cai intermediare
    currState = branches.pop()
    tempPath = []

    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for child, direction, cost in successors:
                branches.push(child) # adaugam stare copil in coada pt a fi explorata mai tarziu
                tempPath.append(direction) # calea temp pt a ajunge de la succesor la calea curenta
                pathToCurr.push(tempPath) # salvam calea temp in coada
        currState = branches.pop() # exploram urmatoarea stare
        path = pathToCurr.pop() # scoatem starea curenta din coada

    return path

# BFS care ia in calcul si costurile
 # prioritatea e determinata de costul total de la starea initiala la starea curenta
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    branches = util.PriorityQueue() # tine evidenta starilor de explorat
    branches.push(problem.getStartState(), 0)
    visited = []
    path = []
    pathToCurr = util.PriorityQueue() # coada cu prioritate pt cai intermediare
    currState = branches.pop() # starea cu cel mai mic cost din coada branches
    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for child, direction, cost in successors:
                tempPath = path + [direction] # cale temp cu directia catre succesor
                costToGo = problem.getCostOfActions(tempPath) # costul total pt a ajunge la succesor
                if child not in visited:
                    branches.push(child, costToGo) # adaugam succesorul in coada cu prioritate costToGo
                    pathToCurr.push(tempPath, costToGo) # adaugam calea catre succesor in coada
        currState = branches.pop() # scoatem starea cu cel mai mic cost pt a fi explorata in continuare
        path = pathToCurr.pop() # scoatem calea asociata cu starea curenta
    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# mai rapid decat UCS si BFS cand euristica e bine definita

# extinde nodul cu cel mai mic cost
# heuristic reduce nr de stari explorate -> se concentreaza pe directia corecta
# prioritatea in queue e determinata de g(x) + f(x)  ; g(x) = cost drum h(x) = euristica
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    branches = util.PriorityQueue()
    branches.push(problem.getStartState(), 0)
    currState = branches.pop() # scoatem starea cu cel mai mic cost -> incepem explorarea
    visited = []
    path = []
    pathToCurr = util.PriorityQueue() # pt caile asociate fiecarei stari
    while not problem.isGoalState(currState):
        if currState not in visited:
            visited.append(currState)
            successors = problem.getSuccessors(currState)
            for child, direction, cost in successors:
                tempPath = path + [direction] # cale temp cu directia catre succesor
                costToGo = problem.getCostOfActions(tempPath) + heuristic(child, problem) # costul total pt succesor
                if child not in visited:
                    branches.push(child, costToGo) # adaugam succesorul in coada
                    pathToCurr.push(tempPath, costToGo) # salvam calea catre succesor
        currState = branches.pop()
        path = pathToCurr.pop()
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
