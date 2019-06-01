# 8-puzzle
The 8-puzzle consists of a 3×3 board with eight numbered tiles and a blank space which I have taken to be 0. Any tile adjacent to the blank space (0) can slide into the space. The object is to reach a specified goal state which is 
1	2	3
4	5	6
7	8	0

The different states that each action can result in is defined by the location of the eight tiles and blank space because of the action. Starting off with the initial state, which is given as input, we take the possible actions defined for that state which is determined by the location of the blank space. At each new state, we check if the goal state is reached. Path cost is defined as the number of steps in the path which is the number of actions taken to reach the goal state from the initial state.

Best First Search:
In BFS a node is selected for expansion based on the evaluation function f(n). The node with lowest evaluation function is expanded first. So, in the code I have used a list to maintain the states and each time I am sorting it based on the evaluation function f(n). Heuristic functions are the most common form in which additional knowledge of the problem is imparted to the search algorithm. Here we are considering f(n)=h(n) where h(n) is the estimated cost of the cheapest path from that state to the goal state. The heuristic functions h(n) I have considered are the:
1.	Number of misplaced tiles: h(n)= Counting the number of misplaced tiles on the puzzle board after each action. If the initial state was 457812360 the h(n) =8. 
h(n) is an admissible heuristic because it is clear that any tile that is out of place must be moved at least once.
2.	Manhattan distance: h(n)=|correct row-current row|+|correct col- current col|. Summation of the Manhattan distance of all tiles on board after each action. h(n) is admissible because all any move can do is move the tile one step closer to the goal. The manhattan distance heuristic is admissible since it considers each tile independently.
3.	Composite heuristic: 
max (Number of misplaced tiles heuristic, Manhattan distance heuristic)
Since Misplaced tiles heuristic and Manhattan distance heuristic is admissible, a heuristic taking maximum of the two would also be admissible.
The composite heuristic uses whichever heuristic function is most accurate on the state in question.

A* Search:
The most widely known form of best-first search is called A*search. The evaluation function is given as f(n)=g(n)+h(n) where g(n) is the number of actions or path to each that state from the initial state and h(n) is the heuristic function which is the estimated cost of the cheapest path from that state to the goal. A* search is complete and optimal. Because g(n) is the actual cost to reach the state along the current path from the initial state , and f(n)=g(n) + h(n), we have as an immediate consequence that f(n) never overestimates the true cost of a solution along the current path through that state. We need to find a solution or the sequence of actions with the lowest f(n) to reach the goal state from the initial state. A* expands the frontier state of lowest f(n) at each state. I am doing this by maintaining a list and sorting it after frontiers of a state is added. The heuristic functions I have considered are:
1      Number of misplaced tiles:
h(n)= Counting the number of misplaced tiles on the puzzle board after each action.
g(n) is the depth or the number of actions to reach that state from initial state
If the initial state was 457812360 the h(n) =8.
h(n) is an admissible heuristic because it is clear that any tile that is out of place must be moved at least once.
2.	Manhattan distance: sum of the horizontal and vertical distances.
h(n)=|correct row-current row|+|correct col- current col|. Summation of the Manhattan distance of all tiles on board after each action.
g(n) is the depth or the number of actions to reach that state from initial state
h(n) is admissible because all any move can do is move one tile one step closer to the goal.
The Manhattan Distance heuristic is admissible since it considers each tile independently..
3.	Composite heuristic: 
h(n)=max (Number of misplaced tiles heuristic, Manhattan distance heuristic)
g(n) is the depth or the number of actions to reach that state from initial state.
Since Misplaced tiles heuristic and Manhattan distance heuristic is admissible, a heuristic taking maximum of the two would also be admissible.
The composite heuristic uses whichever heuristic function is most accurate on the state in question.

Conclusion:
Average taken over 5 randomly generated initial boards. 
Best First Search Misplaced Tiles: Average Number of steps 31.6
Best First Search Manhattan Distance: Average Number of steps 38.0
Best First Search Composite heuristic: Average Number of steps 38.0
A* Misplaced Tiles: Average Number of steps 18.4
A* Manhattan Distance: Average Number of steps 18.4
A*Composite heuristic Average Number of steps 18.4

The A* and Best First Search have been run on 5 inputs. The inputs and the goal state are hardcoded into the program. To test with user input you can use takeuserinput() function instead of calling the main function. Average number of steps is taken over the 5 inputs given to 6 algorithms individually.
As we can observe from the above output, A* takes a smaller number of steps to reach the goal state than Best First Search. A* does not overestimate the number of steps to reach the goal state, it ends up expanding only the nodes that are in the path to the goal state. As the Best First Search is a greedy approach it expands to states having less cost in its frontier and thus, we have a greater number of states obtained to reach the goal state. 

From the three heuristics we can conclude that misplaced tiles take less or equal number of steps as Manhattan distance and composite heuristic. We can say that the manhattan distance heuristic approximates the actual number of steps better than the misplaced tiles heuristic. The manhattan distance heuristic will generate less states in the search tree is because it will be able to approximate which states to explore next better than the misplaced tile heuristic.
We can say that heuristic function of manhattan distance dominates the heuristic function of misplaced. h(manhattan)>=h(misplaced). This because h(manhattan) expands more nodes than h(misplaced). h(manhattan) is at least as big as h(misplaced) for all states since every node expanded by h(manhattan) will also surely be expanded with h(misplaced). 
Th composite heuristic picks the manhattan distance heuristic most of the time since it gives a better approximation of the actual number of steps than misplaced tiles heuristic.
Hence, we can say that A* has a better performance than greedy BFS.

References: Artificial Intelligence: A Modern Approach Textbook by Peter Norvig and Stuart J. Russell



