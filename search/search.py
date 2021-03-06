# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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

def searchAlgorithm(problem, fringe, heuristic=None):
    
    #The Basic Search Algorithm remains same , only the way the fringe is handled changes. 
    #Our method needs three elements problem,fringe,heuristic. Heuristic is none except Astar.
    #In DFS the fringe is stored as LIFO that is why Stack is implemented
    #In BFS the fringe is stored as FIFO that is why Queue is implemented
    #In UCS the fringe is stored as Priority Queue as it implements a least cost method
    #In Astar the fringe is stored as UCS but with heuristic.Heuristic is passed by the method.
    
    #maintain a list of nodes which have been explored, you will need to check this before proceeding
    explored_nodes = [] 
    #maintain a list of actions that is to be followed
    actionlist = []  

    if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue): 
        #check for DFS or BFS , DFS maintains a Stack and BFS maintains a Queue 
        fringe.push((problem.getStartState(), actionlist))
    elif isinstance(fringe, util.PriorityQueue):
        #for ucs and acs a Priority Queue is the solution, but here the heuristic needs to be pushed too
        fringe.push((problem.getStartState(), actionlist), heuristic(problem.getStartState(), problem))
    
    #check the nodes in the fringe 
    while fringe :   
        
        #get the node
        node, actions = fringe.pop()
        
        #check if node is already explored.
        if not node in explored_nodes:
            #add to the list of explored nodes
            explored_nodes.append(node)
            #check if goal is reached
            if problem.isGoalState(node):
            #Succes
                return actions
            #If its not the goal , get successors
            successors = problem.getSuccessors(node)
            #now iterate the succesors
            for successor in successors:
                #get the coordinates            
                coordinate = successor[0]
                #get the directs
                direction = successor[1]
                #create new actions 
                newAction = actions + [direction]
                
                #Check if DFS/BFS or UCS/Astar 
                if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
                    #Push the new Coordinates and new action to the fringe.
                    fringe.push((coordinate, newAction))

                elif isinstance(fringe, util.PriorityQueue):
                    #Calculate the new cost for UCS/Astar using the Heuristic function
                    newCost = problem.getCostOfActions(newAction) + heuristic(coordinate, problem)
                    #Push the new coordinate,new action,new cost to the fringe
                    fringe.push((coordinate, newAction), newCost)                  

    return []
    
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
    #The Basic Search Algorithm remains same , only the way the fringe is handled changes.
    #In DFS the fringe is stored as LIFO that is why Stack is implemented
    return searchAlgorithm(problem, util.Stack())

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    #The Basic Search Algorithm remains same , only the way the fringe is handled changes.
    #In BFS the fringe is stored as FIFO that is why Queue is implemented
    return searchAlgorithm(problem, util.Queue())

def uniformCostSearch(problem):
    "Search the node of least total cost first. "

    return aStarSearch(problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
   
    return searchAlgorithm(problem, util.PriorityQueue(), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
