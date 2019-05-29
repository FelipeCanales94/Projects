''' 
Nils Napp
Sliding Probelm for AI-Class
'''

from slideproblem import *
import time
import heapq


## you likely need to inport some more modules to do the serach


class Searches:

    def tree_bfs(self, problem):
        # reset the node counter for profiling
        Node.nodeCount = 0
        n = Node(None, None, 0, problem.initialState)
        print(n)
        frontier = [n]
        while len(frontier) > 0:
            n = frontier.pop(0)
            for a in p.applicable(n.state):
                nc = child_node(n, a, p)
                if nc.state == p.goalState:
                    return solution(nc)
                else:
                    frontier.append(nc)

    def graph_bfs(self, problem):
        Node.nodeCount = 0
        n = Node(None, None, 0, problem.initialState)
        print(n)
        frontier = [n]

        explored = set()

        while len(frontier) > 0:
            n = frontier.pop(0)
            for a in p.applicable(n.state):
                nc = child_node(n, a, p)
                if nc.state == p.goalState:
                    print(nc.cost)
                    return solution(nc)
                else:
                    childState = nc.state.toTuple()
                    if not (childState in explored):
                        frontier.append(nc)
                        explored.add(childState)

    def recursiveDL_DFS(self, lim, problem):
        n = Node(None, None, 0, problem.initialState)
        return self.depthLimitedDFS(n, lim, problem)

    def depthLimitedDFS(self, n, lim, problem):

        # reasons to cut off brnaches
        if n.state == problem.goalState:
            return solution(n)
        elif lim == 0:
            return None

        cutoff = False
        for a in p.applicable(n.state):
            nc = child_node(n, a, problem)
            result = self.depthLimitedDFS(nc, lim - 1, problem)

            if not result == None:
                return result

        return None

    def id_dfs(self, problem):

        Node.nodeCount = 0

        maxLim = 32
        for d in range(1, maxLim):
            result = self.recursiveDL_DFS(d, problem)
            if not result == None:
                return result
        print('Hit max limit of ' + str(maxLim))
        return None

    def h_1(self, s0: State, sf: State) -> numbers.Real:

        # Number of misplaced items

        misplaced = 0

        for i in range(3):
            for j in range(3):
                if s0.board[i][j] != sf.board[i][j] and s0.board[i][j] != 0 and sf.board[i][j]:
                    misplaced = misplaced + 1
        return misplaced

    def h_2(self, s0: State, sf: State) -> numbers.Real:

        # Manhattan Distance

        rowMoves = abs(sf.position[0] - s0.position[0])
        columnMoves = abs(sf.position[1] - s0.position[1])

        totalMoves = columnMoves + rowMoves

        return totalMoves

    def a_star_tree(self, problem: Problem) -> tuple:

        Node.nodeCount = 0  # Initialize node count to 0

        n = Node(None, None, 0, problem.initialState)  # Create new node (Root Node) with initial state
        frontier = [n]  # Initialize frontier with just n as its only element

        while frontier:  # Keep going until frontier is empty or we find a solution
            heapq.heapify(frontier)
            n = heapq.heappop(frontier)  # pop first element in frontier --- FIFO

            if p.goalTest(n.state):  # if n is a solution, return it
                return solution(n)
            else:

                for action in p.applicable(n.state):  # for every action that n can do
                    child = child_node(n, action, p)  # child node of n with only one action n can make

                    if p.goalTest(child.state):  # if child is goal state, return child
                        return solution(child)
                    child.f = child.cost + self.h_1(child.state, problem.goalState)  # update heuristic
                    heapq.heappush(frontier, child)  # put child with new heuristic in frontier

    def a_star_graph(self, problem: Problem) -> tuple:

        Node.nodeCount = 0  # Initialize node count to 0

        n = Node(None, None, 0, problem.initialState)  # Create new node (Root Node) with initial state
        frontier = [n]  # Initialize frontier with just n as its only element
        explored = set([])  # Initialized an explored set

        while frontier:  # Keep going until frontier is empty or we find a solution
            heapq.heapify(frontier)
            n = heapq.heappop(frontier)  # pop first element in frontier --- FIFO
            explored.add(n.state.toTuple())  # explored must keep track of elements in frontier (makes runtime quicker)
            self.h_1(n.state, problem.goalState)

            if problem.goalTest(n.state):  # if n is a solution, return it
                return solution(n)
            else:

                for action in problem.applicable(n.state):  # for every action that n can do
                    child = child_node(n, action, problem)  # child node of n with only one action n can make

                    if problem.goalTest(child.state):  # if child is goal state, return child
                        return solution(child)
                    if child.state.toTuple() not in explored:  # if child has not been explored yet
                        child.f = child.cost + self.h_1(child.state, problem.goalState)  # update heuristic
                        heapq.heappush(frontier, child)  # put child with new heuristic in frontier
                        explored.add(child.state.toTuple())  # gotta keep track of frontier elements



import time

p = Problem()
s = State()
n = Node(None, None, 0, s)
n2 = Node(n, None, 0, s)

searches = Searches()

p.goalState = State(s)

p.apply('R', s)
p.apply('R', s)
p.apply('D', s)
p.apply('D', s)
p.apply('L', s)

p.initialState = State(s)

print(p.initialState)

si = State(s)
# change the number of random moves appropriately
# If you are curious see if you get a solution >30 moves. The 
apply_rnd_moves(12, si, p)
p.initialState = si

startTime = time.clock()

print('=== Bfs*  ===')
startTime = time.clock()
res = searches.graph_bfs(p)
print(res)
print(time.clock() - startTime)
print(Node.nodeCount)



print('=== id DFS*  ===')
startTime = time.clock()
res = searches.id_dfs(p)
print(res)
print(time.clock() - startTime)
print(Node.nodeCount)

print('\n\n=== A*-Tree ===\n')
startTime = time.clock()
res = searches.a_star_tree(p)
print(time.clock() - startTime)
print(Node.nodeCount)
print(res)

print('\n\n=== A*-Graph ===\n')
startTime = time.clock()
res = searches.a_star_graph(p)
print(time.clock() - startTime)
print(Node.nodeCount)
print(res)

