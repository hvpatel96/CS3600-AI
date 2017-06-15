# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from game import Directions
    if problem.isGoalState(problem.getStartState()):
        return []
    destinationDict = dict()
    destinationDict[problem.getStartState()] = problem.getStartState(), Directions.STOP
    frontier = util.Stack()
    visited = set()
    children = problem.getSuccessors(problem.getStartState())
    for child in children:
        frontier.push(child[0])
        destinationDict[child[0]] = problem.getStartState(), child[1]
    while not frontier.isEmpty():
        currentNode = frontier.pop()
        visited.add(currentNode)
        children = problem.getSuccessors(currentNode)
        for child in children:
            if child[0] not in visited:
                frontier.push(child[0])
                destinationDict[child[0]] = currentNode, child[1]
                if problem.isGoalState(child[0]):
                    answer = list()
                    current = child[0]
                    while current != problem.getStartState():
                        answer.append(destinationDict[current][1])
                        current = destinationDict[current][0]
                    return list(reversed(answer))


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    from game import Directions
    if problem.isGoalState(problem.getStartState()):
        return []
    destinationDict = dict()
    destinationDict[problem.getStartState()] = problem.getStartState(), Directions.STOP
    frontier = util.Queue()
    visited = set()
    visited.add(problem.getStartState())
    children = problem.getSuccessors(problem.getStartState())
    for child in children:
        frontier.push(child[0])
        destinationDict[child[0]] = problem.getStartState(), child[1]
    while not frontier.isEmpty():
        currentNode = frontier.pop()
        if currentNode not in visited:
            visited.add(currentNode)
            if problem.isGoalState(currentNode):
                answer = list()
                current = currentNode
                while current != problem.getStartState():
                    answer.append(destinationDict[current][1])
                    current = destinationDict[current][0]
                return list(reversed(answer))
            children = problem.getSuccessors(currentNode)
            for child in children:
                if child[0] not in visited:
                    frontier.push(child[0])
                    if child[0] not in destinationDict.keys():
                        destinationDict[child[0]] = currentNode, child[1]


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    from game import Directions
    if problem.isGoalState(problem.getStartState()):
        return []
    destinationDict = dict()
    destinationDict[problem.getStartState()] = problem.getStartState(), Directions.STOP, 0
    frontier = util.PriorityQueue()
    visited = set()
    visited.add(problem.getStartState())
    children = problem.getSuccessors(problem.getStartState())
    for child in children:
        destinationDict[child[0]] = problem.getStartState(), child[1], child[2]
        pathCost = problem.getCostOfActions(getPath(destinationDict, child[0], problem.getStartState()))
        frontier.push(child[0], pathCost)
    while not frontier.isEmpty():
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode):
            return getPath(destinationDict, currentNode, problem.getStartState())
        if currentNode not in visited:
            visited.add(currentNode)
            children = problem.getSuccessors(currentNode)
            for child in children:
                if child[0] not in visited:
                    pathCost = problem.getCostOfActions(getPath(destinationDict, currentNode, problem.getStartState())) + child[2]
                    if destinationDict.get(child[0]) is None or destinationDict.get(child[0])[2] > pathCost:
                        destinationDict[child[0]] = currentNode, child[1], pathCost
                    frontier.push(child[0], pathCost)


def getPath(dict, startingNode, stopNode):
    path = list()
    while startingNode != stopNode:
        path.append(dict[startingNode][1])
        startingNode = dict[startingNode][0]
    return list(reversed(path))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    from game import Directions
    if problem.isGoalState(problem.getStartState()):
        return []
    destinationDict = dict()
    destinationDict[problem.getStartState()] = problem.getStartState(), Directions.STOP, 0
    frontier = util.PriorityQueue()
    visited = set()
    visited.add(problem.getStartState())
    children = problem.getSuccessors(problem.getStartState())
    for child in children:
        destinationDict[child[0]] = problem.getStartState(), child[1], child[2]
        pathCost = problem.getCostOfActions(getPath(destinationDict, child[0], problem.getStartState())) + heuristic(child[0], problem)
        frontier.push(child[0], pathCost)
    while not frontier.isEmpty():
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode):
            return getPath(destinationDict, currentNode, problem.getStartState())
        if currentNode not in visited:
            visited.add(currentNode)
            children = problem.getSuccessors(currentNode)
            for child in children:
                if child[0] not in visited:
                    pathCost = problem.getCostOfActions(getPath(destinationDict, currentNode, problem.getStartState())) + child[2] + heuristic(child[0], problem)
                    if destinationDict.get(child[0]) is None or destinationDict.get(child[0])[2] > pathCost:
                        destinationDict[child[0]] = currentNode, child[1], pathCost
                    frontier.push(child[0], pathCost)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
