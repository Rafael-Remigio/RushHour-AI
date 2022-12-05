
import math

import copy

import time



import heapq

class MyHeap(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        self.index = 0
        if initial:
            self._data = [(key(item), i, item) for i, item in enumerate(initial)]
            self.index = len(self._data)
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self._data)[2]



# Methods





def stringToGrid(mapString):
    """Initializes Map Tuple from a MapString Representation"""
    mapString = mapString.split(" ")[1]
    grid_size = int(math.sqrt(len(mapString)))
    pieceSet = []
    grid = []
    line = []
    for i, pos in enumerate(mapString):

        # Creates an Array with all the diferent Pieces
        if (pos not in {"o","x"} ) and (pos not in pieceSet):
            pieceSet.append(pos)
        
        #
        line.append(pos)
        if (i + 1) % grid_size == 0:
            grid.append(line)
            line = []

    return (grid,pieceSet,"")


    

def stringToGridA(mapString):
    """Initializes Map Tuple from a MapString Representation and initializes cost at 0"""
    mapString = mapString.split(" ")[1]
    grid_size = int(math.sqrt(len(mapString)))
    pieceSet = []
    grid = []
    line = []
    for i, pos in enumerate(mapString):

        # Creates an Array with all the diferent Pieces
        if (pos not in {"o","x"} ) and (pos not in pieceSet):
            pieceSet.append(pos)
        
        #
        line.append(pos)
        if (i + 1) % grid_size == 0:
            grid.append(line)
            line = []

    return (grid,pieceSet,"",0)


def coordinates(grid):
    """Representation of ocupied map positions through tuples x,y,carValue."""
    _coordinates = []
    
    for y, line in enumerate(grid):
        for x, column in enumerate(line):
            if column != "o":
                _coordinates.append((x, y, column))

    return _coordinates
    


def piece_coordinates(piece: str,_coordinates):
    """List coordinates holding a piece from coordinates"""
    return [(x, y) for (x, y, p) in _coordinates if p == piece]




def canMove(grid, piece: str, direction,_piece_coordinates):
    """Bolean on if a movement is available given by a piece and a vector tuple."""
    gridSize = len(grid)


    def sum(a, b):
        return (a[0] + b[0], a[1] + b[1])
    
    def locationAvailable(cur):
        if 0 <= cur[0] < gridSize and 0 <= cur[1] < gridSize:
            if grid[cur[1]][cur[0]] in [piece, "o"]:
                return True
            else:
                return False
        return False

    piece_coord = _piece_coordinates
    
    
    for pos in piece_coord:
        if locationAvailable(sum(pos, direction)) == False:
            return False

    return True



def move(grid,piece,piece_coords,vector):
    """Grid (2d Char Array) of a move of a certain piece"""

    def sum(a, b):
        return (a[0] + b[0], a[1] + b[1])

    for coord in piece_coords:
        grid[coord[1]][coord[0]] = "o"

    for coord in piece_coords:
        cursor = sum(coord,vector)
        grid[cursor[1]][cursor[0]] = piece
    
    return




def test_win(grid):
    """Test if player_car has crossed the left most column."""

    grid_size = len(grid)
    
    return any(
        [c[0] == grid_size - 1 for c in piece_coordinates("A",coordinates(grid))]
    )



def possibleMoves(map):
    """List of possible foward states from a given Map Tuple"""
    possibleStates = []

    _coordinates = coordinates(grid=map[0])

    for car in map[1]:
        carCords = piece_coordinates(car,_coordinates)

        if carCords[0][1] == carCords[1][1]:

            if canMove(map[0],car,(-1,0),carCords):

                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(-1,0))

                map2 = (grid2,map[1],map[2] + car + "a")  # Creates a copy of the current Map Tuple and Updates the current Solution


                
                possibleStates.append(map2) # Appends it to the possible states


            if canMove(map[0],car,(1,0),carCords):



                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(1,0))

                map2 = (grid2,map[1],map[2] + car + "d")  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states

                
        else:
            if canMove(map[0],car,(0,-1),carCords):


                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(0,-1))


                map2 = (grid2,map[1],map[2] + car + "w")  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states


            if canMove(map[0],car,(0,1),carCords):


                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(0,1))

                map2 = (grid2,map[1],map[2] + car + "s")  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states



    return possibleStates


def DistanceToExitEuristics(grid,_coordinates):

    grid_size = len(grid)

    cords = piece_coordinates("A",_coordinates)[1]


    return grid_size - cords[0]



def DistanceToExitBlockingCars(grid,_coordinates):

    grid_size = len(grid)

    cords = piece_coordinates("A",_coordinates)[1]

    grid_size - cords[0]
    array = [(x,cords[1]) for x in range(grid_size - cords[0])]
    counter = 0
    for i in _coordinates:
        if (i[0],i[1]) in array:
            counter+=1
        

    return grid_size - cords[0] + counter



def possibleMovesAStart(map):
    """List of possible foward states from a given Map Tuple"""
    possibleStates = []

    _coordinates = coordinates(grid=map[0])

    for car in map[1]:
        carCords = piece_coordinates(car,_coordinates)

        if carCords[0][1] == carCords[1][1]:

            if canMove(map[0],car,(-1,0),carCords):

                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(-1,0))

                map2 = (grid2,map[1],map[2] + car + "a",DistanceToExitBlockingCars(grid2,_coordinates))  # Creates a copy of the current Map Tuple and Updates the current Solution


                
                possibleStates.append(map2) # Appends it to the possible states


            if canMove(map[0],car,(1,0),carCords):



                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(1,0))

                map2 = (grid2,map[1],map[2] + car + "d",DistanceToExitBlockingCars(grid2,_coordinates))  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states

                
        else:
            if canMove(map[0],car,(0,-1),carCords):


                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(0,-1))


                map2 = (grid2,map[1],map[2] + car + "w",DistanceToExitBlockingCars(grid2,_coordinates))  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states


            if canMove(map[0],car,(0,1),carCords):


                grid2 = copy.deepcopy(map[0])
                move(grid2,car,carCords,(0,1))

                map2 = (grid2,map[1],map[2] + car + "s",DistanceToExitBlockingCars(grid2,_coordinates))  # Creates a copy of the current Map Tuple and Updates the current Solution

                
                possibleStates.append(map2) # Appends it to the possible states



    return possibleStates



def breathsearch(startState):
    mapa = stringToGrid(startState)
    open_nodes = [mapa]
    visitedNodes = set()
    while open_nodes != []:

        node = open_nodes.pop(0)

        if test_win(node[0]):
            solution = node
            print("open nodes ->",len(visitedNodes))
            return solution[2]


        for a in possibleMoves(node):
            if not visitedNodes.__contains__(str(a[0])):
                open_nodes.append(a)
                visitedNodes.add(str(a[0]))



    return None



def AStar(startState):
    mapa = stringToGridA(startState) # returns a tuple with a cost starting at 0
    open_nodes = MyHeap([mapa],key=lambda x: x[3]) # Uses  a heap to keep the nodes sorted
    visitedNodes = set()


    while open_nodes != []:

        node = open_nodes.pop()

        if test_win(node[0]):
            solution = node
            print("open nodes ->",len(visitedNodes))
            return solution[2]


        for a in possibleMovesAStart(node):
            if not visitedNodes.__contains__(str(a[0])):
                open_nodes.push(a) # Pushes on to the heap. keeps the nodes sorted
                visitedNodes.add(str(a[0]))



    return None




if __name__ == "__main__":
    
    file1 = open('levels.txt', 'r')
    Lines = file1.readlines()
    j =1
    startTime = 0
    endTime = 0
    searchType = "A*"
    for i in Lines:

        if searchType == "breathSearch":
            startTime = time.time()
            breathsearch(i)
            endTime = time.time()

        if searchType == "A*":
            startTime = time.time()
            AStar(i)
            endTime = time.time()
    
    
        #print("level nº " + str(j) + " time is " + str(endTime - startTime) + " seconds")
        j+=1
