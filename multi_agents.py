from queue import PriorityQueue
import copy


starting_board = [[2, 0, 2, 0, 2, 0],
                  [0, 0, 0, 2, 1, 2],
                  [1, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 1, 0],
                  [2, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0]]

goal_board = [[2, 0, 2, 0, 0, 0],
              [0, 0, 0, 2, 1, 2],
              [1, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 1, 2],
              [0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0]]




def find_agents_locations(board):
    agents_locations = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 2:
                agents_locations.append((i, j))  # append location (x,y)
    return agents_locations


def h(current_board, goal):
    # Our hieuristic

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


def check_if_action_is_okay(agents_positions):
    original_length = len(agents_positions)
    set_length = len(set(agents_positions))
    return set_length == original_length


def convert_to_tuples(board):
    return tuple(map(tuple, board))


def print_route(node):

    # Print the route we came from
    if node is None:
        return

    for row in node[3]:
        print(row)
    print()
    print_route(node[4])


def a_star(board, goal):

    explored = set()
    inside_frontier = set() # board that are currently inside the frontier

    # key -> board that is inside explored, value -> (f(x), g(x), h(x))
    cost_so_far = {}
    came_from = {}

    # f(x), g(x), h(x), board, state(Where we came from)
    node = (0, 0, 0, board, None)
    frontier = PriorityQueue()
    frontier.put(node)
    inside_frontier.add(convert_to_tuples(node[3]))
    g_tup = convert_to_tuples(goal) # goal board presented as tuple
    goal_num_agents = len(find_agents_locations(goal)) # number of agents in the goal board

    while not frontier.empty():
       
        node = frontier.get()
        exp = convert_to_tuples(node[3])
  

        if exp == g_tup:
            # TODO: return success
            print_route(node)
            return True

       
        explored.add(exp)
        inside_frontier.remove(exp)
        cost_so_far[exp] = (node[0], node[1], node[2])
        came_from[exp] = node[4]
        b = node[3]


        # Indexes of agents in board of current node.
        agent_indexes = find_agents_locations(b)

        actions = []

        def find_all_actions(boar, agents, i=0, new_agents=[]):
            # checking optipons to move
            if i >= len(agents):
                s = set(new_agents)
                if len(s) == len(agents):
                    actions.append(tuple(new_agents))
                return

            x, y = agents[i]

            find_all_actions(boar, agents, i=i+1,
                             new_agents=new_agents + [(x+1, y)])
            find_all_actions(boar, agents, i=i+1,
                             new_agents=new_agents + [(x, y+1)])
            find_all_actions(boar, agents, i=i+1,
                             new_agents=new_agents + [(x, y-1)])
            find_all_actions(boar, agents, i=i+1,
                             new_agents=new_agents + [(x-1, y)])

        print(len(actions))
        find_all_actions(b, agent_indexes)
        # actions = set(tuple(actions))k

        for action in actions:

            if not check_if_action_is_okay(action):
                continue

            # The board that holds the new indexes of the agents that moved one step
            new_b = copy.deepcopy(b)

            # Insert the new positions of the agents into the new board
            flag = False

            for index in range(len(agent_indexes)):
                x, y = agent_indexes[index]
                new_x, new_y = action[index]
                new_b[x][y] = 0
                if not new_x < 0 and not new_y < 0:

                    # If the index is out of bounds, abort and do nothing
                    try:
                        if new_b[new_x][new_y] == 1:
                            flag = True
                            break
                        new_b[new_x][new_y] = 2

                    except Exception as e:
                        # print(e)
                        pass

            if (not goal_num_agents == len(find_agents_locations(new_b))) or flag:
                continue

            b_tup = convert_to_tuples(new_b)

            if b_tup not in explored and b_tup not in inside_frontier:
                new_heuristic = h(new_b, goal_board)

                new_fx = 1 + node[1] + new_heuristic
                new_node = (new_fx, 1 + node[1], new_heuristic, new_b, node)
                frontier.put(new_node)
                inside_frontier.add(b_tup)

      
            elif b_tup in explored:

                before_value = cost_so_far[b_tup][1]
                new_value = 1 + node[1]  # g(x)
                if new_value < before_value:
                    came_from[b_tup] = node

    # frontier is empty... didn't find solution
    return False


print(a_star(starting_board, goal_board))
