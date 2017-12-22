# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        curr_state_food_len=currentGameState.getNumFood()
        cur_state_food=currentGameState.getFood().asList()
        new_state_food_len = successorGameState.getNumFood()
        final_score=successorGameState.getScore()

        if action is Directions.STOP:
            final_score=final_score-3
        if successorGameState.isWin():
            return float("inf")
        if len(successorGameState.getFood()[0])==0:
            final_score=final_score-1
        for C in currentGameState.getCapsules():
            if newPos == C:
                final_score= final_score+1500
            else:
                final_score= final_score+(1.0/(manhattanDistance(newPos,C)))
        if curr_state_food_len>new_state_food_len:
            final_score=final_score+200
        else:
            final_score=final_score-1
        for item in cur_state_food:
            dist=manhattanDistance((item),newPos)
            if dist==0:
                final_score=final_score+200
            else:
                final_score=final_score+(1.0/dist)
        for ghost in newGhostStates:
            ghost_curPos=ghost.getPosition()
            if((manhattanDistance(ghost_curPos,newPos)<=1)):
                if ghost.scaredTimer==0:
                    final_score=final_score-200
                else:
                    final_score=final_score+1000

        return final_score

        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minMax(self,State,depth,A_index=0):
        if State.isWin() or State.isLose() or depth == 0:
            return (self.evaluationFunction(State), )
        res = []
        for act in State.getLegalActions(A_index):
            nextState = State.generateSuccessor(A_index, act)
            next_A_index = (A_index + 1) % (State.getNumAgents())
            next_depth = depth
            if A_index == (State.getNumAgents() - 1):
                next_depth = depth - 1
            score=self.minMax(nextState,next_depth,next_A_index)
            res.append((score[0],act))
        if A_index!=0:
            return min(res)
        return max(res)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        return self.minMax(gameState,self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def maxAgent(state, agentIndex, currDepth, alpha, beta):
            #self.numNodeExpanded += 1
            best_max_val = (float("-inf"), "Stop")
            for action in state.getLegalActions(agentIndex):
                nextState = state.generateSuccessor(agentIndex,action)
                newIndex = (currDepth + 1) % numAgents  # newIndex be 0 after all ghosts have completed their turns
                newDepth = currDepth + 1
                new_val = (utility(nextState, newIndex,newDepth,alpha,beta),action)
                best_max_val = max([best_max_val,new_val],key=func)  # get max on basis of utility value
                alpha = max(alpha, best_max_val[0])
                if alpha > beta:
                    return best_max_val
            return best_max_val

        def minAgent(state, agentIndex, currDepth, alpha, beta):
            self.numNodeExpanded += 1
            best_min_val = (float("inf"), "Stop")
            for action in state.getLegalActions(agentIndex):
                nextState = state.generateSuccessor(agentIndex, action)
                newIndex = (currDepth + 1) % numAgents
                newDepth = currDepth + 1
                new_val = (utility(nextState, newIndex, newDepth, alpha, beta), action)
                best_min_val = min([best_min_val,new_val],key=func)  # get min on basis of utility value
                beta = min(beta, best_min_val[0])
                if alpha > beta:
                    return best_min_val
            return best_min_val

        def utility(state, agentIndex, currDepth, alpha, beta):
            if state.isLose() or state.isWin() or currDepth >= depth * numAgents:
                #print "number of node expanded %d" %self.numNodeExpanded
                return self.evaluationFunction(state)
            if (agentIndex == 0):  # pacman
                return maxAgent(state, agentIndex, currDepth, alpha, beta)[0]
            else:  # ghosts
                return minAgent(state, agentIndex, currDepth, alpha, beta)[0]

        self.numNodeExpanded = 0
        numAgents = gameState.getNumAgents()
        depth = self.depth
        pac_agent_index = 0
        func = lambda vals: vals[0]  # func for comparing two nodes on basis of utility values
        return maxAgent(gameState, pac_agent_index, 0, float("-inf"), float("inf"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def maxVal(state, agentIndex, currDepth):
            best_max_val = (float("-inf"), "Stop")
            actions = state.getLegalActions(agentIndex)
            for action in actions:
                nextState = state.generateSuccessor(agentIndex, action)
                newIndex = (currDepth + 1) % numAgents
                newDepth = currDepth + 1
                new_val = (utility(nextState,newIndex, newDepth),action)
                best_max_val = max([best_max_val, new_val],key=func)
            return best_max_val

        def expVal(state, agentIndex, currDepth):
            expectedValue = [0.0]  # list of values for children of a node
            actions = state.getLegalActions(agentIndex)  # all the possible legal moves
            for action in actions:
                nextState = state.generateSuccessor(agentIndex, action)  # get the successor state
                newIndex = (currDepth + 1) % numAgents  # turn for next agent
                newDepth = currDepth + 1
                # utility value of each leaf node to be added to give the expected value of a min node and
                # ghosts decides on the basis of this expected value whether to take that path or not..
                expectedValue.append(utility(nextState, newIndex, newDepth))
            return sum(expectedValue) / (len(expectedValue) - 1)  # returning the average

        def utility(state, agentIndex, currDepth):
            if state.isLose() or state.isWin() or currDepth >= depth * numAgents:
                return self.evaluationFunction(state)
            if (agentIndex == 0): # 0 for pacman
                return maxVal(state, agentIndex, currDepth)[0]
            else:  # for ghosts
                return expVal(state, agentIndex, currDepth)

        # using (value,action)
        numAgents = gameState.getNumAgents()
        depth = self.depth
        pacIndex = 0
        func = lambda vals: vals[0]  # func for comparing two nodes on basis of utility values
        return maxVal(gameState, pacIndex, 0)[1]  # returns list of actions
        # values = [values(s') for s' in successors(s)]
        # weights = [probability(s,s') for s' in successors(s')]
        # return expectations(values,weights)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

