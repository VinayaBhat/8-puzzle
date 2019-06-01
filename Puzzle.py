import random
import math

#maximum number of states that can be explored
total_moves = 10000

#desired final state of the puzzle board
goalstate = [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 0]]

#list to maintain the final average of all 3 heuristic using BFS and A*.
finalaverage=[0,0,0,0,0,0]

#correct location of the tiles based on the goal state
correct_position={
    1:(0,0),
    2:(0,1),
    3:(0,2),
    4:(1,0),
    5:(1,1),
    6:(1,2),
    7:(2,0),
    8:(2,1),
    0:(2,2)
}

class EightPuzzleBoard:

    def __init__(self):
        #The previous state which led to the current state. For intial state the parentstate is None
        self.parentstate = None
        #heurisitc value
        self.hfunc = 0
        #depth or distance from intial state
        self.gfunc = 0
        #an instance of the 3x3 board
        self.puzzleboard = []
        for i in range(3):
            self.puzzleboard.append(goalstate[i][:])

     #overiding function to equate puzzle board instances
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.puzzleboard == other.puzzleboard

#convert the input string read from the user input to a 3x3 puzzle board
    def convertInputtoPuzzleBoard(self, values):
        i = 0;
        for row in range(3):
            for col in range(3):
                self.puzzleboard[row][col] = int(values[i])
                i = i + 1

#clone the current instance of the 3x3 board
    def copyInstance(self):
        p = EightPuzzleBoard()
        for i in range(3):
            p.puzzleboard[i] = self.puzzleboard[i][:]
        return p

#Given a unique value on a 3x3 board return its row and column number in the 3x3 matrix representation
    def getRowandCol(self, value):
        if value < 0 or value > 8:
            raise Exception("Number not on board")

        for row in range(3):
            for col in range(3):
                if self.puzzleboard[row][col] == value:
                    return row, col

#Given the row and column number of a 3x3 matrix return the value present in that location
    def getValue(self, row, col):
        return self.puzzleboard[row][col]

#Given the row and column number of a 3x3 matrix set the value present in that location to the one given in input
    def setValue(self, row, col, value):
        self.puzzleboard[row][col] = value

#Swapping the values in position_a and position_b eg: position_a=(1,2) value =3
    # and position_b=(2,1) value=4, after swapping position_a will have 4 and position_b will have 3
    def swappingvalues(self, position_a, position_b):
        temp = self.getValue(*position_a)
        self.setValue(position_a[0], position_a[1], self.getValue(*position_b))
        self.setValue(position_b[0], position_b[1], temp)

#The function gets the position of the blank tile (0) and calculates the allowed moves of the blank tile on a 3x3 board for that position.
    def allowedblankmoves(self):
        row, col = self.getRowandCol(0)
        blank_moves = []
        if row > 0:
            blank_moves.append((row - 1, col)) #up
        if col > 0:
            blank_moves.append((row, col - 1)) #left
        if row < 2:
            blank_moves.append((row + 1, col)) #down
        if col < 2:
            blank_moves.append((row, col + 1)) #right
        return blank_moves

#The fucntion uses the allowedblankmoves fucntion and return the resulting states after applying each of the allowed blank moves.
    def resultingstates(self):
        moves = self.allowedblankmoves()
        zero_coord = self.getRowandCol(0)
        def swapandcopy(a, b):
            puzzle = self.copyInstance()
            puzzle.swappingvalues(a, b)
            puzzle.gfunc = self.gfunc + 1
            puzzle.parentstate = self
            return puzzle
        return map(lambda move_coord: swapandcopy(zero_coord, move_coord), moves)

#Given the goalstate traverse back the path from the goalstate to the initial state
    def traverseBackPath(self, path):
        if self.parentstate == None:
            return path
        else:
            path.append(self)
            return self.parentstate.traverseBackPath(path)

#A* search algorithm
    def aStar(self, heuristic_function):
        def solved(puzzle_instance): # to check if the current state is the goal state
            return puzzle_instance.puzzleboard == goalstate
        openlist = [self] #to keep track of states yet to be considered
        closedlist = [] #to keep track of states considered
        no_of_states = 0 #moves to different state
        initialstate=self.puzzleboard
        while len(openlist) > 0:
            current_state = openlist.pop(0)
            no_of_states =no_of_states+1

            if (no_of_states > total_moves): #if the number of moves exceed the limit then return
                print("Exceeded maximum number of moves: ",total_moves)
                return [], no_of_states

            if (solved(current_state)): # if the current state is the goalstate return the goal state and number of states considerd to reach the goal state
                if len(closedlist) > 0:
                    return current_state.traverseBackPath([]), no_of_states
                else:
                    move_count=0 #if the initial state is goal state return the inital state and number of moves
                    return [current_state],move_count
            next_possible_states = current_state.resultingstates() #get the next states after moving the blank tile
            for state in next_possible_states: #for each if the possible next states
                openlist_index = puzzle_state_exists(state, openlist) #check if the state exists in openlist
                closedlist_index = puzzle_state_exists(state, closedlist) #check if the states exists in closed list
                hval = heuristic_function(state) #calculate the heuristic value
                fval = hval + state.gfunc  # calculate the evaluation funciton f(n)=h(n)+g(n)
                if closedlist_index == -1 and openlist_index == -1: #if the state is not in openlist or blanklist
                    state.hfunc = hval
                    openlist.append(state) #add state to openlist
                elif openlist_index > -1:  #if state is already in openlist
                    clone_state = openlist[openlist_index]  #get the state from open list
                    if fval < clone_state.hfunc + clone_state.gfunc: #compare the new f value of the state with existing f value
                        clone_state.hfunc = hval
                        clone_state.parentstate = state.parentstate
                        clone_state.gfunc = state.gfunc
                elif closedlist_index > -1: #if state is already in closedlist
                    clone_state = closedlist[closedlist_index]  #get the state from closedlist
                    if fval < clone_state.hfunc + clone_state.gfunc: #compare the new f value of the state with existing f value
                        state.hfunc = hval
                        closedlist.remove(clone_state)   #remove the state from closed list
                        openlist.append(state)           #add state to open list
            closedlist.append(current_state)            #add state to closed list after visiting all its frontiers
            openlist = sorted(openlist, key=lambda p: p.hfunc + p.gfunc) #sort the openlist on evaluation function
        return [], no_of_states  #return if openlist becomes empty

#Best First Search algorithm
    def bestFirstSearch(self, heuristic_function):
        def solved(puzzle):
            return puzzle.puzzleboard == goalstate
        openlist = [self]
        closedlist = []
        no_of_states = 0
        while len(openlist) > 0:
            current_state = openlist.pop(0)
            no_of_states = no_of_states+1

            if (no_of_states > total_moves):
                print("Exceeded maximum number of moves: ",total_moves)
                return [], no_of_states

            if (solved(current_state)):
                if len(closedlist) > 0:
                    return current_state.traverseBackPath([]), no_of_states
                else:
                    return [current_state],no_of_states

            next_possible_states = current_state.resultingstates()
            openlist_index = closedlist_index = -1
            for state in next_possible_states:
                openlist_index = puzzle_state_exists(state, openlist)
                closedlist_index = puzzle_state_exists(state, closedlist)
                hval = heuristic_function(state)
                fval = hval #f(n)=h(n)
                if closedlist_index == -1 and openlist_index == -1:
                    state.hfunc = hval
                    openlist.append(state)
                elif openlist_index > -1:
                    clone_state = openlist[openlist_index]
                    if fval < clone_state.hfunc:
                        clone_state.hfunc = hval
                        clone_state.parentstate = state.parentstate
                elif closedlist_index > -1:
                    clone_state = closedlist[closedlist_index]
                    if fval < clone_state.hfunc:
                        state.hfunc = hval
                        closedlist.remove(clone_state)
                        openlist.append(state)
            closedlist.append(current_state)
            openlist = sorted(openlist, key=lambda p: p.hfunc)
        return [], no_of_states

#return the index of the state if the state exits in the list else return -1
def puzzle_state_exists(current_instance, list):
    if current_instance in list:
        return list.index(current_instance)
    else:
        return -1

#**********************************************************************Heuristics******************************************************#
#Common heuristic function: Calculates the correct row and column of each tile

def heuristic_Calculation(puzzle_instance, function1, function2):
    total = 0
    for row in range(3):
        for col in range(3):
            value = puzzle_instance.getValue(row, col)
            location=correct_position[value] #get the correct location of the tile from the dictionary correct_position
            correct_row=location[0] #get row
            correct_col=location[1] #get column
            total += function1(row, correct_row, col, correct_col)
    return function2(total)

# Misplaced tiles heuristic returns the number of tiles out of place in the given state/instance of the board
def heuristic_misplacedtiles(puzzle_instance):
    def misplaced_tiles_count(puzzle_instance):
        count = 0
        for row in range(3):
            for col in range(3):
                if (puzzle_instance.getValue(row, col) != goalstate[row][col]): #if the tile present in the location of current instance
                    # does not match the tile in the goal state
                    count = count + 1
        return count
    answer=misplaced_tiles_count(puzzle_instance)
    return answer

# Manhattan distanceheuristic: |current_row-correct_row|+ |current_col-correct_col| of each tile
def heuristic_manhattandistance(puzzle_instance):
    return heuristic_Calculation(puzzle_instance,lambda curr_row, corr_row, curr_col, corr_col: abs(corr_row - curr_row) + abs(corr_col - curr_col),lambda answer: answer)

#Composite function heuristic: h(n)=max(h_misplaced_tile(n),h_manhattandistance(n))
def heuristic_compositefunction(puzzle_instance):
    h_misplacedtiles=heuristic_misplacedtiles(puzzle_instance)
    h_manhattandistance=heuristic_manhattandistance(puzzle_instance)
    maximum=max(h_manhattandistance,h_misplacedtiles)
    return maximum

#print the path from initials state to goal state
def printStepstoSolve(solvedpath,puzzle_board):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in puzzle_board]))
    for path in solvedpath:
        print(path.puzzleboard)

#Solve the puzzle using A* and BFS using 3 different heurisitic
def solvepuzzle(puzzle_instance):
    print("************* BEST FIRST SEARCH USING MISPLACED TILES HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.bestFirstSearch(heuristic_misplacedtiles)
    print("Initial state of puzzle board:")
    if (solvedpath != []):
        solvedpath.reverse() #reverse path to get from inital state to goal state path
        printStepstoSolve(solvedpath, puzzle_instance.puzzleboard)
        finalaverage[0]=finalaverage[0]+len(solvedpath) #sum the number of steps to calculate the average
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states, "states")
    else:
        print("BEST FIRST SEARCH search has stopped after going through", no_of_states - 1, "states")

    print("************* BEST FIRST SEARCH  SEARCH USING MANHATTAN DISTANCE HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.bestFirstSearch(heuristic_manhattandistance)
    if (solvedpath != []):
        solvedpath.reverse()
        printStepstoSolve(solvedpath, puzzle_instance.puzzleboard)
        finalaverage[1]=finalaverage[1]+len(solvedpath)
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states, "states")
    else:
        print("BEST FIRST SEARCH search has stopped after going through", no_of_states - 1, "states")

    print("************* BEST FIRST SEARCH USING COMPOSITE FUNCTION HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.bestFirstSearch(heuristic_compositefunction)
    if (solvedpath != []):
        solvedpath.reverse()
        printStepstoSolve(solvedpath, puzzle_instance.puzzleboard)
        finalaverage[2]=finalaverage[2]+len(solvedpath)
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states, "states")
    else:
        print("BEST FIRST SEARCH search has stopped after going through", no_of_states - 1, "states")
#######################################################################################################
    print("************* A* SEARCH USING MISPLACED TILES HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.aStar(heuristic_misplacedtiles)
    print("Initial state of puzzle board:")
    if (solvedpath != []):
        solvedpath.reverse()
        printStepstoSolve(solvedpath,puzzle_instance.puzzleboard)
        finalaverage[3]=finalaverage[3]+len(solvedpath)
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states,"states")
    else:
        print("A* search has stopped after going through" , no_of_states - 1, "states")

    print("************* A* SEARCH USING MANHATTAN DISTANCE HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.aStar(heuristic_manhattandistance)
    if (solvedpath != []):
        solvedpath.reverse()
        printStepstoSolve(solvedpath,puzzle_instance.puzzleboard)
        finalaverage[4]=finalaverage[4]+len(solvedpath)
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states,"states")
    else:
        print("A* search has stopped after going through" , no_of_states - 1, "states")

    print("************* A* SEARCH USING COMPOSITE FUNCTION HEURISTIC ******************")
    solvedpath, no_of_states = puzzle_instance.aStar(heuristic_compositefunction)
    if (solvedpath != []):
        solvedpath.reverse()
        printStepstoSolve(solvedpath,puzzle_instance.puzzleboard)
        finalaverage[5]=finalaverage[5]+len(solvedpath)
        print("Solved  8 puzzle in ", len(solvedpath), "steps after exploring", no_of_states, "states")
    else:
        print("A* search has stopped after going through", no_of_states - 1, "states")

#to take initial state from user input
def takeuserinput():
    input_string=input("Enter the initial state of the puzzle (eg 4567890123) :")
    puzzle=EightPuzzleBoard()
    puzzle.convertInputtoPuzzleBoard(input_string)
    solvepuzzle(puzzle)

def main():
    puzzle = EightPuzzleBoard() #initializing the puzzle instance
    puzzle.convertInputtoPuzzleBoard("457812360") #converting the string input to matrix
    solvepuzzle(puzzle) #solving the puzzle using A* and BFS
    print("**************************************************************************************************************************************")
    puzzle.convertInputtoPuzzleBoard("123457806")
    solvepuzzle(puzzle)
    print("**************************************************************************************************************************************")
    puzzle.convertInputtoPuzzleBoard("012345678")
    solvepuzzle(puzzle)
    print("**************************************************************************************************************************************")
    puzzle.convertInputtoPuzzleBoard("365214780")
    solvepuzzle(puzzle)
    print("**************************************************************************************************************************************")
    puzzle.convertInputtoPuzzleBoard("125043687")
    solvepuzzle(puzzle)
    for i in range(0,6):
        finalaverage[i]=finalaverage[i]/5
    print("Best First Search Misplaced Tiles: Average Number of steps ",finalaverage[0])
    print("Best First Search Manhattan Distance: Average Number of steps ",finalaverage[1])
    print("Best First Search Composite function: Average Number of steps ",finalaverage[2])
    print("A* Misplaced Tiles: Average Number of steps ",finalaverage[3])
    print("A* Manhattan Distance: Average Number of steps ",finalaverage[4])
    print("A*Composite function Average Number of steps ",finalaverage[5])


if __name__ == "__main__":
    main() #to test hardcoded input
    #takeuserinput() # to test with user input