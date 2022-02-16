


def print_route(node):

    '''
        Print the route we came from
    '''
    if node is None:
        return

    for row in node[3]:
        print(row)
    print()
    print_route(node[4])


def check_if_action_is_okay(agents_positions):

    '''
    Params
    ------
    agents_positions: List of tuples containing the agent locations




    output
    ----- 
    True if none of the agents are overlapping each other.


    '''

    original_length = len(agents_positions)
    set_length = len(set(agents_positions))
    return set_length == original_length



def h(current_board, goal):

    '''
    ---- HEURISTIC ----

    Uses the sum of the euclidean distance of each current agent position to its goal state position 


    params
    ------
    current_board: List of list of ints. The currect state of the board
    goal: List of list of ints. The goal state of the board
    
    

    output
    ------
    A number representing the heuristic distance from the goal state
    '''


    def calc_heuristic_for_each_agent(start_loc, goal_loc):
        # Find the distance between two agents
        return abs(goal_loc[0] - start_loc[0]) + abs(goal_loc[1] - start_loc[1])

    # Find the indexes of all agents in the current_board and the goal_board
    index_agents_current = []
    index_agents_goal = []

    index_agents_current = find_agents_locations(current_board)
    index_agents_goal = find_agents_locations(goal)
    max_dist = float('-inf')  # This is our longest distance

    for i in range(len(index_agents_current)):
        dist = calc_heuristic_for_each_agent(
            index_agents_current[i], index_agents_goal[i])  # distance between two agents
        if dist > max_dist:
            max_dist = dist
    return max_dist


def find_agents_locations(board):
    '''
    params
    ------
    board: list of list of ints. The state of the game


    output
    ------
    List of tuples of x and y representing the location of each agent in the board
    
    '''

    agents_locations = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 2:
                agents_locations.append((i, j))  # append location (x,y)
    return agents_locations



