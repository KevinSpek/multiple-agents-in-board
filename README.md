# Multiple Agents In Board

A board contains free squares, agents and obstacles. Agents can move up, down, left and right we the square next to him is free. They are **not** allowed to move on top of obstacles and not on top of other agents. 
A typical board is represented as an array:
```
[0, 0, 1, 0]
[0, 2, 0, 0]
[1, 2, 0, 0]
```

* Zero is a free spot
* One is an agent
* Two is an obstacle
## The Task

Given a board, and a goal board, the agents must find the optimal path to get to their correct position in the gold state.

#### The solution is an A* algorithm that uses the Euclidean distance between each agent location and the desired goal location, by calculating all possible solutions for each state.

## How To Use

Inside the `data.py` file place your `starting_board` state and  the `goal_board` state and run `python main.py` command in terminal to let the magic begin!
