from util import manhattanDistance
from game import Directions
import random
import util
from typing import Any, DefaultDict, List, Set, Tuple

from game import Agent
from pacman import GameState



class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def __init__(self):
        self.lastPositions = []
        self.dc = None

    def getAction(self, gameState: GameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions(agentIndex):
            Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor state after the specified agent takes the action.
            Pac-Man is always agent 0.

        gameState.getPacmanState():
            Returns an AgentState object for pacman (in game.py)
            state.configuration.pos gives the current position
            state.direction gives the travel vector

        gameState.getGhostStates():
            Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
            Returns the total number of agents in the game

        gameState.getScore():
            Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action: str) -> float:
        """
        The evaluation function takes in the current GameState (defined in pacman.py)
        and a proposed action and returns a rough estimate of the resulting successor
        GameState's value.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (problem 1)
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction. Terminal states can be found by one of the following:
          pacman won, pacman lost or there are no legal moves.

          Don't forget to limit the search depth using self.depth. Also, avoid modifying
          self.depth directly (e.g., when implementing depth-limited search) since it
          is a member variable that should stay fixed throughout runtime.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.getScore():
            Returns the score corresponding to the current state of the game

          gameState.isWin():
            Returns True if it's a winning state

          gameState.isLose():
            Returns True if it's a losing state

          self.depth:
            The depth to which search should continue

        """

        # BEGIN_YOUR_CODE (our solution is 22 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        

        def Vminmax(state: GameState, depth: int, agentIndex: int) -> float:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pac-Man's turn (Max)
                bestValue = float("-inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    bestValue = max(bestValue, Vminmax(successor, depth, agentIndex + 1))
                return bestValue
            else:  # Ghosts' turns (Min)
                nextAgent = (agentIndex + 1) % state.getNumAgents()
                if nextAgent == 0:
                    depth += 1  # Increment depth when it's Pac-Man's turn
                worstValue = float("inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    worstValue = min(worstValue, Vminmax(successor, depth, nextAgent))
                return worstValue

        legalActions = gameState.getLegalActions(0)  # Pac-Man's legal actions
        bestAction = None
        bestValue = float("-inf")

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = Vminmax(successor, 0, 1)  # Start with depth 0 and agentIndex 1 (ghosts)
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction
        
        # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (problem 2)
      You may reference the pseudocode for Alpha-Beta pruning here:
      en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        # BEGIN_YOUR_CODE (our solution is 43 lines of code, but don't worry if you deviate from this)
        # raise Exception("Not implemented yet")
        
        def alphaBetaPruning(state: GameState, depth: int, alpha: float, beta: float, agentIndex: int) -> float:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pac-Man's turn (Max)
                bestValue = float("-inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = alphaBetaPruning(successor, depth, alpha, beta, agentIndex + 1)
                    bestValue = max(bestValue, value)
                    alpha = max(alpha, bestValue)
                    if bestValue > beta:
                        return bestValue
                return bestValue
            else:  # Ghosts' turns (Min)
                nextAgent = (agentIndex + 1) % state.getNumAgents()
                if nextAgent == 0:
                    depth += 1  # Increment depth when it's Pac-Man's turn
                worstValue = float("inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = alphaBetaPruning(successor, depth, alpha, beta, nextAgent)
                    worstValue = min(worstValue, value)
                    beta = min(beta, worstValue)
                    if worstValue < alpha:
                        return worstValue
                return worstValue

        legalActions = gameState.getLegalActions(0)  # Pac-Man's legal actions
        bestAction = None
        bestValue = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = alphaBetaPruning(successor, 0, alpha, beta, 1)  # Start with depth 0 and agentIndex 1 (ghosts)
            if value > bestValue:
                bestValue = value
                bestAction = action
            alpha = max(alpha, bestValue)

        return bestAction
        
        
        # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax


class ExpectimaxAgent(MultiAgentSearchAgent):
    
     

    def getAction(self, gameState: GameState) -> str:
        
        """
          Your expectimax agent (problem 3)
        """
        
        """
           Returns the expectimax action using self.depth and self.evaluationFunction
        
           All ghosts should be modeled as choosing uniformly at random from their
           legal moves.
         """

         # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
         # raise Exception("Not implemented yet")
        
        
        def expectimaxSearch(state: GameState, depth: int, agentIndex: int) -> float:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:  # Pac-Man's turn
                maxAction = None
                maxValue = float("-inf")
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = expectimaxSearch(successor, depth, agentIndex + 1)
                    if value > maxValue:
                        maxValue = value
                        maxAction = action
                return maxValue

            else:  # Ghosts' turns (Random Ghosts)
                nextAgent = (agentIndex + 1) % state.getNumAgents()
                if nextAgent == 0:
                    depth += 1
                expectedValue = 0
                numActions = len(state.getLegalActions(agentIndex))
                probability = 1.0 / numActions
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    value = expectimaxSearch(successor, depth, nextAgent)
                    expectedValue += probability * value
                return expectedValue

        legalActions = gameState.getLegalActions(0)  # Pac-Man's legal actions
        bestAction = None
        bestValue = float("-inf")

        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            value = expectimaxSearch(successor, 0, 1)  # Start with depth 0 and agentIndex 1 (ghosts)
            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction

   
     
     
     # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function


def betterEvaluationFunction(currentGameState: GameState) -> float:
    """
      Your extreme, unstoppable evaluation function (problem 4). Note that you can't fix a seed in this function.
    """

    # BEGIN_YOUR_CODE (our solution is 16 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE


# Abbreviation
better = betterEvaluationFunction
