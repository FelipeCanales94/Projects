import numpy as np
from markov import *
from drawprob import pList, pShow, robotShow


class MDPSillyGame:
    def __init__(self):
        self.domsize = 160
        self.reward = self._mkreward()

        self.eps = 0.05  # <--- CHANGE ME

        self.A = self.transitionMatrix(self.eps)
        self.value = self._mkreward()

        ''' 
        Change this answer 
        You shoul play if you have equal or more than this amount
        '''
        self.cutoff = 81  # <--- your answer here

    def _mkreward(self):
        reward = np.arange(self.domsize)
        for i in range(100, self.domsize):
            reward[i] = reward[i] + 50
        return reward

    def transitionMatrix(self, eps):
        '''put code here to compute the transition matrix '''
        A = np.zeros([self.domsize, self.domsize])

        for idx in range(self.domsize):
            A[idx, idx] = eps

            if idx > 0:
                A[(idx-1), idx] = 0.5
            else:
                A[idx, idx] += 0.5

            if 0 < idx < (self.domsize - 1):
                A[(idx+1), idx] = (0.5 - eps)
            else:
                A[idx, idx] += (0.5 - eps)

        return A

    def valIter(self):

        '''
        These are the two options 
        When you stop, you can cash out the reward
        when you plan, the you can win or lose 
        '''

        vstop = self.reward
        vplay = np.zeros(self.domsize)

        for i in range(self.domsize):
            vplay[i] = np.dot(self.A[:, i], self.value)  # <--Note how this is computed

        self.value = np.amax(np.array([vstop, vplay]), axis=0)
        return vplay, self.value


# Actions of Maze problem
actions = ['up', 'left', 'down', 'right', 'stop']


class MDPMaze:
    def __init__(self, maze, stateReward):

        self.maze = maze
        self.stateReward = stateReward
        self.stateSize = maze.stateSize
        self.stateReward.resize(self.stateSize)

        self.eps = 0.30
        self.gamma = 0.9
        self.rewardM = np.ones(self.stateSize) * (-1)

        # place holders for computing transition matrices
        Aup, Aleft, Adown, Aright, Astop = self.computeTransitionMatrices()

        self.Aup = Aup
        self.Aleft = Aleft
        self.Adown = Adown
        self.Aright = Aright
        self.Astop = Astop

        self.value = np.zeros(self.stateSize)
        self.policy = []

    # You can use this to construct the noisy matrices
    def ARandomWalk(self):
        A = np.zeros((self.stateSize, self.stateSize))

        for col in range(self.stateSize):
            nbrs = self.maze.nbrList(col)
            p = 1 / (len(nbrs) + 1)
            A[col, col] = p
            for r in nbrs:
                A[r, col] = p
        return A

    def computeTransitionMatrices(self):
        '''put code here to initialize the matrices '''
        Aup = ((1 - self.eps) * self.actionMatrix('up')) + self.eps * self.ARandomWalk()
        Aleft = ((1 - self.eps) * self.actionMatrix('left')) + self.eps * self.ARandomWalk()
        Adown = ((1 - self.eps) * self.actionMatrix('down')) + self.eps * self.ARandomWalk()
        Aright = ((1 - self.eps) * self.actionMatrix('right')) + self.eps * self.ARandomWalk()
        Astop = self.actionMatrix('stop')

        return Aup, Aleft, Adown, Aright, Astop

    def actionMatrix(self, actions):
        A = np.zeros((self.stateSize, self.stateSize))

        for col in range(self.stateSize):
            c_r, c_c = self.maze.state2coord(col)
            row = None
            if actions == 'up':
                if c_r - 1 >= 0 and self.maze.world[c_r - 1, c_c] != 1:
                    row = self.maze.coord2state([c_r - 1, c_c])
                else:
                    row = col

            elif actions == 'left':
                if c_c - 1 >= 0 and self.maze.world[c_r, c_c - 1] != 1:
                    row = self.maze.coord2state([c_r, c_c - 1])
                else:
                    row = col

            elif actions == 'down':
                if c_r + 1 < self.maze.worldShape[0] and self.maze.world[c_r + 1, c_c] != 1:
                    row = self.maze.coord2state([c_r + 1, c_c])
                else:
                    row = col

            elif actions == 'right':
                if c_c + 1 < self.maze.worldShape[1] and self.maze.world[c_r, c_c + 1] != 1:
                    row = self.maze.coord2state([c_r, min(c_c + 1, self.maze.worldShape[1] - 1)])
                else:
                    row = col

            elif actions == 'stop':
                row = col

            if row is not None:
                A[row, col] = 1

        return A

    def valIter(self):
        ''' This should update self.value'''
        value = np.array(self.value.copy())
        rw = self.rewardM + self.stateReward

        for i in range(self.stateSize):
            sum_up = rw[i] + self.gamma * np.dot(self.Aup[:, i], value)
            sum_down = rw[i] + self.gamma * np.dot(self.Adown[:, i], value)
            sum_left = rw[i] + self.gamma * np.dot(self.Aleft[:, i], value)
            sum_right = rw[i] + self.gamma * np.dot(self.Aright[:, i], value)
            sum_stop = self.stateReward[i] + self.gamma * np.dot(self.Astop[:, i], value)

            self.value[i] = np.amax(np.array([sum_up, sum_down, sum_left, sum_right, sum_stop]), axis=0)
        self.computePolity()


    def computePolity(self):
        '''write some code here'''
        #actions = ['up', 'left', 'down', 'right', 'stop']
        self.policy = []  # This shoule be a list so

        value = np.array(self.value.copy())
        rw = self.rewardM + self.stateReward

        for i in range(self.stateSize):
            sum_up = rw[i] + self.gamma * np.dot(self.Aup[:, i], value)
            sum_down = rw[i] + self.gamma * np.dot(self.Adown[:, i], value)
            sum_left = rw[i] + self.gamma * np.dot(self.Aleft[:, i], value)
            sum_right = rw[i] + self.gamma * np.dot(self.Aright[:, i], value)
            sum_stop = self.stateReward[i] + self.gamma * np.dot(self.Astop[:, i], value)

            self.policy.append(actions[np.argmax(np.array([sum_up, sum_left, sum_down, sum_right, sum_stop]), axis=0)])

if __name__ == "__main__":

    ''' silly game '''
    N = 200  # <-change me to get convergence

    gambling = MDPSillyGame()
    for i in range(N):
        vplay, vn = gambling.valIter()
    print('V_stop\tV_play\tmax_u V_n')
    for i in range(60, 110):
        print(gambling.reward[i], '\t', vplay[i], '\t', vn[i])

    ''' MAZE MDP '''

    myMaze = maze(np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]))

    stateReward = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 100, 0, 0, 0, 0, 0],
        [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]])

    mdp = MDPMaze(myMaze, stateReward)

    iterCount = 100
    printSkip = 10

    for i in range(iterCount):
        mdp.valIter()
        if np.mod(i, printSkip) == 0:
            print("Iteration ", i)
            pShow(mdp.value, myMaze)
