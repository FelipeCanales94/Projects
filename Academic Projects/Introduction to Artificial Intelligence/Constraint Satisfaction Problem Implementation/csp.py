import sudoku
import time
import heapq


class Solver:

    def AC3(self, csp, queue=None, removals=None):

        '''
        your code here
        '''

        queue = []  # queue of arms
        heapq.heapify(queue)  # heapify to make it quicker

        # Book/Slide implementations
        for n in csp.neighbors:
            for m in csp.neighbors[n]:
                heapq.heappush(queue, [n, m])
        while queue:
            first = heapq.heappop(queue)
            if self.revise(csp, first[0], first[1], removals):
                if len(csp.curr_domains[first[0]]) is 0:
                    return False
                for xk in csp.neighbors[first[0]]:
                    heapq.heappush(queue, [xk, first[0]])
        return True

    def revise(self, csp, Xi, Xj, removals):
        """Return true if we remove a value."""
        '''
        your code here
        '''

        # Book/Slide implementation
        revised = False

        for n in csp.curr_domains[Xi]:  # Grab all neighbors of Xi
            aConstraint = False  # Constraint boolean
            for m in csp.curr_domains[Xj]:  # Grab all neighbors of Xj
                if csp.constraints(Xi, n, Xj, m):  # Check if there is a constraint
                    aConstraint = True  # set boolean to true if there exists a constrain
            if aConstraint is False:  # if not, prune it
                csp.prune(Xi, n, removals)
                revised = True  # set revise to true

        return revised

    def backtracking_search(self, csp):
        '''
        your code here
        '''

        return self.backtrack({}, csp)

    def backtrack(self, assignment, csp):

        # Book/slides implementation

        if csp.goal_test(assignment):  # check for goal state
            return assignment
        for n in csp.curr_domains:  # check for not in assignment
            if n not in assignment:
                var = n
                break

        for value in csp.curr_domains[var]:
            if csp.nconflicts(var, value, assignment) is 0:                 # no conflicts
                csp.assign(var, value, assignment)                          # add var and value to assignment
                inferences = csp.suppose(var, value)                        # inference steps
                checker = self.AC3(csp, None, inferences)
                if checker:
                    result = self.backtrack(assignment, csp)
                    if result:
                        return result
                csp.unassign(var, assignment)
                csp.restore(inferences)

        return None

if __name__ == '__main__':
    '''
    Some board test cases, each string is a flat enumeration of all the board positions
    where . indicates an unfilled location
    Impossible: 123456789.........123456789123456789123456789123456789123456789123456789123456789
    Easy ..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
    Easy ...7.46.3..38...51.1.9.327..34...76....6.8....62...98..473.6.1.68...13..3.12.5...
    Difficult ..5...1.3....2.........176.7.49....1...8.4...3....7..8.3.5....2....9....4.6...9..
    '''

    board = sudoku.Sudoku('12.456789.........12.45678912.45678912.45678912.45678912.45678912.45678912.456789')
    # Accessing the board as a csp, i.e. display the variable and domains
    # See the extra document for exapmles of how to use the  CSP class

    # Display this nonsensical board
    board.display(board)

    # Show the "flat" variables
    print(board.variables)

    # show the domeians (curr_domains beocmes populated by infer_assignment())
    print(board.curr_domains)

    '''You'll need to manipulate the CSP domains and variables, so here are some exampels'''

    # this is a list of (variable, domain value) pairs that you can use to keep track
    # # of what has been removed from the current domains
    removals = []

    # #show domains for variable 3
    print("Domain for 3: " + str(board.curr_domains[3]))
    # #remove the possible value '8' form domain 3
    # #not the differences int key for the first dictionary and the string keys

    board.prune(3, '8', removals)  # This line may not work if the domain for 3 does not contain "8"

    print("Domain for 3: " + str(board.curr_domains[3]))
    print("Removal List: " + str(removals))

    # Prune some more
    print("Domain for 23: " + str(board.curr_domains[23]))
    board.prune(23, '1', removals)
    board.prune(23, '2', removals)
    board.prune(23, '3', removals)
    print("Domain for 23: " + str(board.curr_domains[23]))
    print("Removal List: " + str(removals))

    # ooopes took away too muche! Restore removals
    board.restore(removals)
    print("Domain for 23: " + str(board.curr_domains[23]))

    # For assigning vaeiables use a dictionary like
    assignment = {}
    board.assign(23, '8', assignment)
    # ocne all the variables are assigned, you can use goal_thest()

    # find the neighbors of a varaible
    print("Neighbors of 0: " + str(board.neighbors[0]))

    # check for a constraint, need to plug in a specific var,val, var val combination
    # since 0 and 1 and neighbors, they should be different values
    print(board.constraints(0, '0', 1, '0'))  # should be valse
    print(board.constraints(0, '0', 1, '1'))  # should be true i.e. not a constraint

    '''to check your implementatios:'''

    # AC3 should return false for impossible example above
    sol = Solver()
    start = time.clock()
    print(sol.AC3(board))
    print("time: " + str(time.clock() - start))
    board.display(board)

    # backtracking search usage example

    print("======================================= BACKTRACKER =======================================")
    start = time.clock()
    sol.backtracking_search(board)
    print("time: " + str(time.clock() - start))
    board.display(board)

