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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    # evalueaza o stare a jocului dupa ce pacman a realizat o actiune
    # selecteaza actiunea cu scorul cel mai mare => returnam cu minus
    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentFood = currentGameState.getFood()
        newPos = successorGameState.getPacmanPosition()

        "*** YOUR CODE HERE ***"

        ghostPositions = successorGameState.getGhostPositions()
        for p in ghostPositions:
            # daca o fantoma e in nextPos sau langa ea (la distanta de 1)
            if p == newPos or util.manhattanDistance(p, newPos) == 1:
                # nu merge acolo - returnam -inf pt a evita alegerea acestei optiuni
                return (float('-inf'))
            # daca este mancare in nextPos si nu avem fantome
            elif currentFood[newPos[0]][newPos[1]]:
                # mergi acolo
                return float('inf')

        # daca pacman nu e in pericol si nu este mancare in poz curenta
        # -> cauta cea mai apropiata bucata de mancare
        minDist = float('inf') # dist pana la cea mai apropiata bucata de mancare
        food = currentFood.asList()
        for f in food:
            dist = util.manhattanDistance(f, newPos)
            if dist < minDist:
                minDist = dist

        # returnam -minDist -> distantele mici devin scoruri mai mari (minDist = 1 devine -1)
        # reurnam minDist -> actiunile care duc pacman mai depare de mancare au scor mai mare
        return -minDist


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

    # aplicam algoritmul Minimax pt a lua decizii, avand scop maximizarea scorului lui pacman
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

        # folosit doar pt pacman => agentindex = 0 mereu
        # pacman vrea sa maximizeze scorul sau - alege actiuni care sa ii ofere cel mai mare scor prin maxLEvel
        def maxLevel(gameState, depth):
            currDepth = depth + 1 # crestem adancimea
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:  # daca stare finala
                return self.evaluationFunction(gameState) # returnam scorul evaluat al starii
            maxvalue = -999999
            actions = gameState.getLegalActions(0) # obtinem toate actiunile pe care pacman le poate efectua
            for action in actions:
                successor = gameState.generateSuccessor(0, action) # noua stare a jocului dupa ce pacman a facut o actiune
                # apoi fac si fantomele o aciune prin minLEvel care returneaza scorul minim pe care fantoma il poate obtine pt pacman
                maxvalue = max(maxvalue, minLevel(successor, currDepth, 1))
            return maxvalue

        # fantomele minimizeaza scroul pt pacman
        def minLevel(gameState, depth, agentIndex):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():  # stare terminala
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex) # obtinem toate actiunile pe care fantoma le poate efectua
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action) # generam o noua stare de joc
                # daca fantoma curenta este ultima
                if agentIndex == (gameState.getNumAgents() - 1):
                    # pacman ia urm decizie - apelam maxLEvel
                    minvalue = min(minvalue, maxLevel(successor, depth))
                else:
                    # apelam minValue pt urm fantoma
                    minvalue = min(minvalue, minLevel(successor, depth, agentIndex + 1))
            # scorul minim pe care fantoma il poate obtine pt pacman
            return minvalue

        # decizia finala
        actions = gameState.getLegalActions(0) # actiunile pt pacman
        currentScore = -999999 # cel mai bun scor gasit
        returnAction = '' # actiunea asociata cu scorul maxim gasit pana la acel moment
        for action in actions:
            nextState = gameState.generateSuccessor(0, action) # generam o noua stare
            score = minLevel(nextState, 0, 1) # actioneaza fantomele
            # alegem actiunea care maximizeaza scorul
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    # minimax cu alpha-beta pruning
    # maximimizeaza scorul pt pacman, minimizeaza scorul pt fantome
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # alpha = cel mai bun scor pe care il poate garanta pacman
        # beta = cel mai rau scor pe care il pot garanta fantomele
        # [alpha, beta] -> limita intre ce poate fi relevant si ce poate fi ignorat

        # pt pacman
        def maxLevel(gameState, depth, alpha, beta):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            alpha1 = alpha # copie pt a putea fi modificata
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                # minLevel - scorul minim pe care fantoma il poate obtine pt pacman
                maxvalue = max(maxvalue, minLevel(successor, currDepth, 1, alpha1, beta))
                # pruning - taierea ramurilor inutile
                # daca maxvalue depaseste beta - nu mai are rost sa continuam
                if maxvalue > beta:
                    return maxvalue
                # actualizam alpha
                alpha1 = max(alpha1, maxvalue)
            return maxvalue

        # pt fantome
        def minLevel(gameState, depth, agentIndex, alpha, beta):
            minvalue = 999999
            if gameState.isWin() or gameState.isLose():  # Terminal Test
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            beta1 = beta
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                # daca e ultima fantoma
                if agentIndex == (gameState.getNumAgents() - 1):
                    # min = min intre min si scorul returnat de pacman
                    minvalue = min(minvalue, maxLevel(successor, depth, alpha, beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1, minvalue)
                else:
                    # apelam pt urm fantoma
                    minvalue = min(minvalue, minLevel(successor, depth, agentIndex + 1, alpha, beta1))
                    if minvalue < alpha:
                        return minvalue
                    beta1 = min(beta1, minvalue)
            return minvalue

        # Alpha-Beta Pruning
        actions = gameState.getLegalActions(0) # actiuni pacman
        currentScore = -999999 # cel mai bun scor gasit
        returnAction = '' # actiunea asociata cu scorul maxim gasit pana la acel moment
        alpha = -999999
        beta = 999999
        for action in actions:
            nextState = gameState.generateSuccessor(0, action) # generam o noua stare
            score = minLevel(nextState, 0, 1, alpha, beta) # evaluaza starea succesorare -> actioneaza fantomele
            # Choosing the action which is Maximum of the successors.
            if score > currentScore:
                returnAction = action
                currentScore = score
            # Updating alpha value at root.
            if score > beta:
                return returnAction
            alpha = max(alpha, score)
        return returnAction

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
        "*** YOUR CODE HERE ***"

        # implementeaza alg Expectimax pt a alege actiunea optima pt pacman avand in vedere ca fantomele aleg miscari aleatorii

        #  modeleaza comportamentul inamicilor (fantomele) ca fiind aleator, in loc de unul optim
        # Este utilizat pentru a determina cea mai buna actiune pentru Pacman, avand in vedere ca fantomele aleg miscari uniform la intamplare.

        # pt pacman
        def maxLevel(gameState, depth):
            currDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or currDepth == self.depth:
                return self.evaluationFunction(gameState)
            maxvalue = -999999
            actions = gameState.getLegalActions(0)
            for action in actions:
                successor = gameState.generateSuccessor(0, action)
                maxvalue = max(maxvalue, expectLevel(successor, currDepth, 1))
            return maxvalue

        # fantomele fac alegeri aleatorii -> foloseste valoare medie a rez posibile
        def expectLevel(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex) # actiunile fantomeloor
            totalexpectedvalue = 0
            numberofactions = len(actions)
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                # ultima fantoma
                if agentIndex == (gameState.getNumAgents() - 1):
                    expectedvalue = maxLevel(successor, depth)
                else:
                    # apelam recursiv pt urmatoarea fantoma
                    expectedvalue = expectLevel(successor, depth, agentIndex + 1)
                totalexpectedvalue = totalexpectedvalue + expectedvalue # acumulam valoarea totala a tuturor actiunilor posibile
            if numberofactions == 0:
                return 0
            return float(totalexpectedvalue) / float(numberofactions) # returnam media valorilor asteptate

        # Root level action.
        actions = gameState.getLegalActions(0) # actiuni pacman
        currentScore = -999999 # cel mai bun scor gasit
        returnAction = '' # actiunea asociata cu scorul maxim gasit pana la acel moment
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)  # generam o noua stare
            score = expectLevel(nextState, 0, 1) # evaluaza starea succesorare -> actioneaza fantomele
            # alegem actiunea cu scorul cel mai bun
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction

# ajuta agentul sa ia decizii intelignete in functie de pozitia fantomelor din joc
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
        In my evaluation function I have divided the final score of the state in two parts
           1. When the ghosts are scared identified scaredTimes>0.
           2. Normal ghosts.
        Common evaluation score between both parts is the sum of the score for current score the steps
          for which the ghosts are scared, the reciprocal of the sum of food distance and number of foods eaten

          In the first case, from the sum I subtract the distance of the ghosts from current state
          and the number of power pellets, as the ghosts are currently in scared state. So closer pacman is to ghost better score

          In the second case since the ghosts are not scared hence distance to ghosts and number of power pellets
          are added to the sum.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood() # pozitia elementelor ramase
    newGhostStates = currentGameState.getGhostStates() # info despre fantome (pozitie + stare - speriate/normale)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # timpul ramas in care fiecare fantoma e speriata; >0 => pacman poate manca fantoma

    # calc dist manhattan intre poz pacman si fiecare aliment inrt-o lista foodList
    foodList = newFood.asList()
    from util import manhattanDistance
    foodDistance = [0]
    for pos in foodList:
        foodDistance.append(manhattanDistance(newPos, pos))

    # calc dist manhattan intre poz pacman si fiecare fantoma intr-o lista ghostDistance
    ghostPos = []
    for ghost in newGhostStates:
        ghostPos.append(ghost.getPosition())
    ghostDistance = [0]
    for pos in ghostPos:
        ghostDistance.append(manhattanDistance(newPos, pos))

    numberofPowerPellets = len(currentGameState.getCapsules()) # nr capsule de putere ramase

    score = 0
    numberOfNoFoods = len(newFood.asList(False))  # nr de mancare ramas
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum(ghostDistance)

    # calc dist pacman fata de alimentele ramase folosind reciprocul distantei totale (1/distanta totala)
    # pt a inversa relatia dintre dist si scor
    # scorul trebuie sa fie mai mare pt starile unde pacman mai aproape de mancare (distanta mica -> reciproc mare)
    reciprocalfoodDistance = 0
    if sum(foodDistance) > 0:
        reciprocalfoodDistance = 1.0 / sum(foodDistance)

    # evaluare scor : scorul curent + apropierea de mancare + nr alimente consumate
    score += currentGameState.getScore() + reciprocalfoodDistance + numberOfNoFoods

    # daca fantomele sunt speriate
    if sumScaredTimes > 0:
        # pacman poate vana fantomele ;
        # + sumScaredTimes - bonus pt timpul in care fantomele raman speriate
        # -1 * numberofPowerPellets - penalizare pt capsulele ramase (incurajeaza pacman sa le foloseasca)
        # -1 * sumGhostDistance - bonus pentru apropierea de fantome (incurajeaza pacman sa le vaneze) -> incurajeaza apropierea de fantome
        score += sumScaredTimes + (-1 * numberofPowerPellets) + (-1 * sumGhostDistance)
    else:
        # pacman trebuie sa evite fantomele
        # +sumGhostDistance - incurajeaza distantarea de fantome
        # +numberofPowerPellets - bonus pentru capuselele ramase
        score += sumGhostDistance + numberofPowerPellets
    return score

# Abbreviation
better = betterEvaluationFunction

