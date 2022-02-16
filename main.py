from queue import PriorityQueue
from utils import print_route, check_if_action_is_okay, h, find_agents_locations
from data import starting_board, goal_board
import copy



def a_star(board, goal):

    def convert_to_tuples(board):
        return tuple(map(tuple, board))

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
            '''
            Finding All possible combinations of next board state recursively
            '''

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



if __name__ == '__main__':
    print(a_star(starting_board, goal_board))
