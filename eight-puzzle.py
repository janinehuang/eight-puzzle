from copy import deepcopy
import heapq
import time

visited_nodes = []
expand_total = 0

class Node():
    def __init__(self, data, depth, heuristic):
        self.data = data
        self.g = 0                  #g(n) cost to get to a node -- maybe use depth cos g is 1 for uniform_cost_search
        self.h = 0                  #h(n) estimated distance to the goal (hardcoded to 0 for uniform_cost_search)
        self.f = self.g + self.h    #f(n) estimated cost of cheapest solution that goes though node n

        self.expand_total = 0
        self.max_q = 0

    def __lt__(self, other):
        return self.f < other.f


def begin():                        #driver function; have user pick a starting puzzle, as well as a choice of algorithm
    matrix = []
    print("Welcome to Janine Huang's 8-puzzle solver.")
    choice = input("Enter \"1\" to to use a default puzzle, or \"2\" to enter your own puzzle. ")
    while ((choice != '1') and (choice != '2')):
        choice = input("Enter \"1\" to to use a default puzzle, or \"2\" to enter your own puzzle. ")
    if choice == '2':               #reference: https://www.geeksforgeeks.org/take-matrix-input-from-user-in-python/
        print("Enter your entries rowwise (use a 0 to represent the blank space):")
        for i in range(3):
            a =[]
            for j in range(3):
                 a.append(int(input()))
            matrix.append(a)
        print("You entered the puzzle: ")
        matrix_print(matrix)
    else:                           #use the default matrix
        matrix = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
        print("\nContinuing with the default puzzle: ")
        for i in range(3):
            for j in range(3):
                print(matrix[i][j], end = " ")
            print()

    print("\nAvailable Algorithms")
    print("\t1. Uniform Cost Search")
    print("\t2. A* with the Misplaced Tile Heuristic")
    print("\t3. A* with the Manhattan Distance Heuristic")
    alg_choice = input("Enter your choice of algorithm: ")

    while ((alg_choice != '1') and (alg_choice != '2') and (alg_choice != '3')):
        alg_choice = input("Enter your choice of algorithm (please pick one of the option above): ")

    initial = Node(matrix, 0, 0)
    if alg_choice == '1':
        start_time = time.time()
        solution = general_search(initial, 1)
        if (solution):
            print_solution(expand_total, solution.max_q, solution.g)
            print("--- %s seconds ---" % (time.time() - start_time))
    elif alg_choice == '2':
        start_time = time.time()
        solution = general_search(initial, 2)
        if (solution):
            print_solution(expand_total, solution.max_q, solution.g)
            print("--- %s seconds ---" % (time.time() - start_time))
    else:
        start_time = time.time()
        solution = general_search(initial, 3)
        if (solution):
            print_solution(expand_total, solution.max_q, solution.g)
            print("--- %s seconds ---" % (time.time() - start_time))

def general_search(initial, alg_choice):
    print("\n**-----Uniform Cost Search START-----**")
    print("Expanding node: ")
    matrix_print(initial.data)
    """
    >>> pseudocode model from lecture slides
    nodes = make_queue(make_node(problem.initial state)
    loop do
        if nodes is empty:
            print ("no solution")
            node = remove front node
        if goalconfirm():
            return node
        nodes = queueing fuction(nodes, expand(node, operators))
    """
    nodes = []
    children = []
    max_queue_nodes = 0
    global expand_total
    heapq.heapify(nodes) #creates the heap queue
    nodes.sort()
    if (alg_choice == 2):
        initial.h = misplaced_tile_heuristic(initial.data)
    elif (alg_choice == 3):
        initial.h = manhattan_distance_heuristic(initial.data)
    else:
        initial.h = 0
    initial.f = initial.g + initial.h
    heapq.heappush(nodes, initial)

    while 1:
        if (len(nodes) == 0):
            print("There is no solution")
            return 0
        cur_node = heapq.heappop(nodes)
        if (len(nodes) > max_queue_nodes):                  #update maximum number of nodes in the queue at any one time, +1 to offset the initial .pop()
            max_queue_nodes = len(nodes) + 1
            cur_node.max_q = max_queue_nodes
        if (goal_confirm(cur_node.data)):
            matrix_print(cur_node.data)
            return cur_node

        zero_posi, zero_posj = find_zero(cur_node)
        if (zero_posi != 0):
            moved_up = move_up(cur_node, alg_choice)
            if (goal_confirm(moved_up.data)):
                matrix_print(moved_up.data)
                return moved_up
            if move_up not in visited_nodes:
                heapq.heappush(nodes, moved_up)
                #print("Moved right:")
                #matrix_print(moved_up.data)
                visited_nodes.append(moved_up)
                expand_total += 1
        if (zero_posi != 2):
            moved_down = move_down(cur_node, alg_choice)
            if (goal_confirm(moved_down.data)):
                matrix_print(moved_down.data)
                return moved_down
            if move_down not in visited_nodes:
                heapq.heappush(nodes, moved_down)
                #print("Moved down:")
                #matrix_print(moved_down.data)
                visited_nodes.append(moved_down)
                expand_total += 1
        if (zero_posj != 0):
            moved_left = move_left(cur_node, alg_choice)
            if (goal_confirm(moved_left.data)):
                matrix_print(moved_left.data)
                return moved_left
            if move_left not in visited_nodes:
                heapq.heappush(nodes, moved_left)
                #print("Moved left:")
                #matrix_print(moved_left.data)
                visited_nodes.append(moved_left)
                expand_total += 1
                #print(len(visited_nodes))
        if (zero_posj != 2):
            moved_right = move_right(cur_node, alg_choice)
            if (goal_confirm(moved_right.data)):
                matrix_print(moved_right.data)
                return moved_right
            if move_right not in visited_nodes:
                heapq.heappush(nodes, moved_right)
                #print("Moved right:")
                #matrix_print(moved_right.data)
                visited_nodes.append(moved_right)
                expand_total += 1

# **********HEURISTIC CALCULATION********** #
def misplaced_tile_heuristic(matrix):
    misplaced = 0
    if (matrix[0][0] != 1):
        misplaced += 1
    if (matrix[0][1] != 2):
        misplaced += 1
    if (matrix[0][2] != 3):
        misplaced += 1
    if (matrix[1][0] != 4):
        misplaced += 1
    if (matrix[1][1] != 5):
        misplaced += 1
    if (matrix[1][2] != 6):
        misplaced += 1
    if (matrix[2][0] != 7):
        misplaced += 1
    if (matrix[2][1] != 8):
        misplaced += 1
    if (matrix[2][2] != 0):
        misplaced += 1
    return misplaced

# Disclaimer: this function does NOT contain original code
# source: https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
def manhattan_distance_heuristic(data):
    matrix = []
    for i in range(3):
        for j in range(3):
            matrix.append(data[i][j])
    return sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
        for i, val in enumerate(matrix) if val)

# ***********OPERATOR FUNCTIONS************* #
def move_up(node, alg_choice):
    zero_posi, zero_posj = find_zero(node)
    node_up = deepcopy(node)
    node_up.g += 1
    if (alg_choice == 2):
        node_up.h = misplaced_tile_heuristic(node_up.data)
    elif (alg_choice == 3):
        node_up.h = manhattan_distance_heuristic(node_up.data)
    else:
        node_up.h = 0
    node_up.f = node_up.g + node_up.h

    temp = node_up.data[zero_posi - 1][zero_posj] #replace with swap function?
    node_up.data[zero_posi - 1][zero_posj] = 0
    node_up.data[zero_posi][zero_posj] = temp
    print("moved up  , current depth is: ", node_up.g)
    matrix_print(node_up.data)
    return node_up         #returns node with 0 moved up

def move_down(node, alg_choice):        #returns node with 0 moved down
    zero_posi, zero_posj = find_zero(node)
    node_down = deepcopy(node)
    node_down.g += 1
    if (alg_choice == 2):
        node_down.h = misplaced_tile_heuristic(node_down.data)
    elif (alg_choice == 3):
        node_down.h = manhattan_distance_heuristic(node_down.data)
    else:
        node_down.h = 0
    node_down.f = node_down.g + node_down.h

    temp = node_down.data[zero_posi + 1][zero_posj] # TODO:replace with swap function?
    node_down.data[zero_posi + 1][zero_posj] = 0
    node_down.data[zero_posi][zero_posj] = temp
    print("moved down, current depth is: ", node_down.g)
    matrix_print(node_down.data)
    return node_down

def move_left(node, alg_choice):
    zero_posi, zero_posj = find_zero(node)
    node_left = deepcopy(node) # use deepcopy to avoid altering original node
    node_left.g += 1
    if (alg_choice == 2):
        node_left.h = misplaced_tile_heuristic(node_left.data)
    elif (alg_choice == 3):
        node_left.h = manhattan_distance_heuristic(node_left.data)
    else:
        node_left.h = 0
    node_left.f = node_left.g + node_left.h

    temp = node_left.data[zero_posi][zero_posj - 1]
    node_left.data[zero_posi][zero_posj - 1] = 0
    node_left.data[zero_posi][zero_posj] = temp
    print("moved left, current depth is: ", node_left.g)
    matrix_print(node_left.data)
    return node_left       #returns node with 0 moved to the left

def move_right(node, alg_choice):       #returns node with 0 moved to the right
    zero_posi, zero_posj = find_zero(node)
    node_right = deepcopy(node)
    node_right.g += 1
    if (alg_choice == 2):
        node_right.h = misplaced_tile_heuristic(node_right.data)
    elif (alg_choice == 3):
        node_right.h = manhattan_distance_heuristic(node_right.data)
    node_right.f = node_right.g + node_right.h

    temp = node_right.data[zero_posi][zero_posj + 1]
    node_right.data[zero_posi][zero_posj + 1] = 0
    node_right.data[zero_posi][zero_posj] = temp
    print("moved right, current depth is: ", node_right.g)
    matrix_print(node_right.data)
    return node_right

# ***********HELPER FUNCTIONS************* #
def find_zero(node):        #locates 0 in the puzzle and returns the indices
    for i in range(3):
        for j in range(3):
            if (node.data[i][j] == 0):
                return i,j

def matrix_print(matrix):   #helper function to "pretty print" the board
    for i in range(3):
        for j in range(3):
            print(matrix[i][j], end = " ")
        print()
    print("\n")

def goal_confirm(matrix):   #helper function to confirm if puzzle passed in matches goal state
    if (matrix == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]):
        return True
    return False

def valid_puzzle(matrix):   # NOT WORKING: helper function to return 0 if user-entered puzzle is missing a 0 or has the invalid character 9
    zero_present = 0
    nine_present = 0
    for i in range(3):
        for j in range(3):
            if (matrix[i][j] == '0'):
                zero_present += 1
            if (matrix[i][j] == '9'):
                nine_present += 1
    if (zero_present == 0 or nine_present == 1):
        return False

def print_solution(expand_total, max_queue_nodes, final_depth):
    print("\nGoal found!")
    print("\nTo solve this puzzle, the search algorithm expanded a total of", expand_total ,"times")
    print("The maximum number of nodes in the queue at any one time was", max_queue_nodes)
    print("The depth of the final goal node is", final_depth)

# **********"int main"************* #
begin()
