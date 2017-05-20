from sys import argv
from time import clock
from copy import deepcopy




class Csp:
    def __init__(self, vars, doms, cons):
        self.vars = vars  # variables
        self.doms = doms  # domains
        self.cons = cons # constrains

def ac3(csp):
    arcs = csp.arcs
    while arcs:
        i, j = arcs.pop()
        if revise(csp, i, j):
            if not csp.doms[i]:
                return False
            for k in csp.neig[i]:
                arcs.add((k, i))
    if any(len(v) > 1 for v in csp.doms.values()):
        return 'not unique!!'
    return True

def revise(csp, i, j):
    revised = False
    for x in csp.doms[i]:
        if not any(csp.cons(x, y) for y in csp.doms[j]):
            csp.doms[i].remove(x)
            revised = True
    return revised

def backtrack_search(csp):
    ac3(csp)
    doms = csp.doms
    assignments = {}
    for var in csp.vars:
        if len(doms[var]) == 1:
            assignments[var] = doms[var]
    return backtrack(assignments, csp)

def backtrack(assignments, csp):
    if len(assignments) == len(csp.vars):
        return assignments
    var = min_rem_val(assignments, csp)
    vars_neig_assig = csp.neig[var] & assignments.keys()
    for val in csp.doms[var]:

        csp_backup = deepcopy(csp)
        assignments_backup = deepcopy(assignments)
        if all(val != csp.doms[v] for v in vars_neig_assig):
            assignments[var] = [val]
            csp.doms[var] = [val]
            if forward_check(csp, var, val):
                result = backtrack(assignments, csp)
                if result is not None:
                    return result
        csp = csp_backup
        assignments = assignments_backup
    return None

def min_rem_val(assignments, csp):
    max = 9
    for var in csp.vars:
        if var not in assignments:
            l = len(csp.doms[var])
            if l <= max:
                max = l
                min = var
    return min


def forward_check(csp, var, val):
    for v in csp.neig[var]:
        if val in csp.doms[v]:
            csp.doms[v].remove(val)
            if len(csp.doms[v]) == 0:
                return False
    return True

class Sudoku(Csp):
# construct sudoku into Csp data structure
    def __init__(self, input):
        def stitch(X, Y):
            return [x + y for x in X for y in Y]
        def box(Z):
            return [Z[i*3:i*3+3] for i in range(3)]
        rows = 'ABCDEFGHI'
        cols = '123456789'
        vars = stitch(rows, cols)
        divisions = ([stitch(rows, col) for col in cols] +
                    [stitch(row, cols) for row in rows] +
                    [stitch(rbox, cbox) for rbox in box(rows) for cbox in box(cols)])
        division = {var : ([u for u in divisions if var in u])
                     for var in vars}
        neig = {var : (set(sum(division[var], [])) - set([var]))
                     for var in vars}
        arcs = set()
        for var in vars:
            for peer in neig[var]:
                arcs.add((var, peer))
        i = 0
        doms = {}
        for var in vars:
            if input[i] == '0':
                doms[var] = list(range(1,10))
            else:
                doms[var] = [int(input[i])]
            i += 1
        def cons(x, y):
            return x != y

        super().__init__(vars, doms, cons)
        self.neig = neig
        self.arcs = arcs

def main():
    csp = Sudoku(argv[1])
    solver2 = backtrack_search(csp)
    s2 = ''
    for var in csp.vars:
        for n in solver2[var]:
            s2 += str(n)
    with open("output.txt", "w") as output:
        output.write(s2)


if __name__ == '__main__':
    # To generate output.txt
    #############################################################
    main()


    # To generate hw_sudoku_UNI.txt
    #############################################################
    # with open('sudokus_start.txt') as input_file:
    #     inputs = [line.rstrip('\r\n') for line in input_file]
    # s1 = ''
    # for n in range(len(inputs)):
    #     for_start = clock()
    #     csp = Sudoku(inputs[n])
    #     solver1 = ac3(csp)
    #     if solver1 == True:
    #         sol = ''
    #         for var in csp.vars:
    #             for val in csp.doms[var]:
    #                         sol += str(val)
    #         s1 += str(n+1)+ '\t\t' + 'running-time = ' + str(clock() - for_start)[:5]+ '\t\t' + 'solution = ' + sol + '\n'
    # with open("hw_sudoku_jh3846.txt", "w") as hw_sudoku_jh3846:
    #     hw_sudoku_jh3846.write(s1)
    #############################################################

    # To test all sudokus_start.txt
    #############################################################
    # with open('sudokus_start.txt') as input_file:
    #     inputs = [line.rstrip('\r\n') for line in input_file]
    # with open('sudokus_finish.txt') as results:
    #     results = [line.rstrip('\r\n') for line in results]
    # s3 = ''
    # for n in range(len(inputs)):
    #     for_start = clock()
    #     csp = Sudoku(inputs[n])
    #     sol = ''
    #     solver3 = backtrack_search(csp)
    #     for var in csp.vars:
    #         for val in solver3[var]:
    #             sol += str(val)
    #     s3 += sol + '\n'
    #     print(n+1, results[n] == sol, sol, clock()-for_start)
    # with open("my_results.txt", "w") as my_results:
    #     my_results.write(s3)
    #############################################################

















