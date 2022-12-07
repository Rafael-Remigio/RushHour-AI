"""Example client."""
import asyncio
import copy
import getpass
import imp
from importlib.resources import path
import json
from mimetypes import common_types
import os
from re import search
import time
from tracemalloc import start
from my_common import Coordinates, Map
# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets



async def agent_loop(server_address="localhost:8080", agent_name="mr_Robot"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        currentlySearching = False
        level = 0
        moves = ''
        mapa = None
        here = 0
        crazyMode = False
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                print(state)
                if state.get('level') != level:
                    level = state.get('level')
                    moves = ''
                    currentlySearching = False
                    mapa = Map(state.get("grid"))
                    mapaString = state.get("grid").split(" ")[1]
                    print(mapaString)

                if not currentlySearching:
                    currentlySearching = True
                    moves =  breathsearch(state.get("grid"))
                    print(moves)
                
                if mapaString != state.get("grid").split(" ")[1]:
                    print("CrazyDriver", state.get("grid").split(" ")[1])
                    crazyMode = True

                    crazyMoves = calculateCrazyMoves(mapaString,state.get("grid").split(" ")[1],mapa)
                    mapa = Map(state.get("grid"))

                if crazyMode:
                    here += 1
                    if crazyMoves == "":
                        crazyMode = False
                        here = 0
                        continue
                    
                    if here == 60:
                        currentlySearching = False
                        level = 0
                        moves = ''
                        crazyMoves = ''
                        mapa = None
                        here = 0
                        crazyMode = False
                        continue

                    mapaString, crazyMoves, key = getNextMove(crazyMoves,state.get("cursor"),mapa,state.get("selected"),mapaString)
                    await websocket.send(json.dumps({"cmd": "key", "key": key})) 



                    continue


                if moves == "":
                    continue
                


                    
                    
                # do the move
                mapaString, moves, key = getNextMove(moves,state.get("cursor"),mapa,state.get("selected"),mapaString)

                await websocket.send(json.dumps({"cmd": "key", "key": key})) 

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


def calculateCrazyMoves(oldMap,newMap,m):

    grid_str = oldMap
    crazy_car = None
    positive = 0
    for i in range(len(oldMap)):
        old_char = grid_str[i]
        new_char = newMap[i]
        # Gets the odd character
        if new_char != old_char:
            crazy_car = old_char if old_char != 'o' else new_char
            positive = -1 if old_char != 'o' else 1

    print(crazy_car,positive)    

    if m.piece_coordinates(crazy_car)[0].y == m.piece_coordinates(crazy_car)[1].y:
        print("horizontal")
        if positive == -1:
            return crazy_car+"d"
        else:
            return crazy_car+"a"

    else:
        print("vertical")

        if positive == -1:
            return crazy_car+"s"
        else:
            return crazy_car+"w"


def getNextMove(moves,cursor,mapa,selected,mapaString):
    
    cursorPos = Coordinates(cursor[0],cursor[1])
    #If a car is selected
    if selected != "":

        # if it is the correct car
        if selected == moves[0]:


            key = moves[1] #selects the move

            mapa.moveWithNoTests(moves[0],letterToCoords(moves[1])) #moves car in the map Object

            moves =  moves[2:]  #removes the move from the grid
            

            # To make this a bit faster in checking the Crazy Drivers
            # This will only change the MapaString variable
            # using the Map.__repr_ method takes O(n)
            # maybe there is a better solution, Problem for future me

            mapaString = mapa.__repr__().split(" ")[1]


            return mapaString, moves,key 

        #if it is the wrong car
        else:
            return mapaString, moves, " "

    # If we are on top of the correct car
    if cursorPos in mapa.piece_coordinates(moves[0]):

        return mapaString, moves, " " #selects that car
    
    # if not on top of the car we need to move to the top of the car
    else:   
        return mapaString, moves, moveCursorToCar(mapa.piece_coordinates(moves[0])[0],cursor)



def letterToCoords(letter):

# Passes from letter move into cursor move for the Map Class

    if letter == "a":
        return Coordinates(-1,0)
    elif letter == "s":
        return Coordinates(0,1)

    elif letter == "d":
        return Coordinates(1,0)

    elif letter == "w":
        return Coordinates(0,-1)
    
    return None

def moveCursorToCar(carCordinates,cursor):

    if carCordinates.x > cursor[0]:
        return "d"
    elif carCordinates.x < cursor[0]:
        return "a"
    elif carCordinates.y > cursor[1]:
        return "s"
    elif carCordinates.y < cursor[1]:
        return "w"
    

def breathsearch(startState):
    open_nodes = [startState]
    visitedNodes = set()
    paths = {startState: ""}
    while open_nodes != []:
        node = open_nodes.pop(0)
        mapa = Map(node)


        if mapa.test_win():
            solution = node
            return paths.get(solution)


        for a in possibleMoves(mapa):
            if not visitedNodes.__contains__(a[0]):
                open_nodes.append(a[0])
                visitedNodes.add(a[0])
                paths[a[0]] = paths.get(node) + a[1]


        #print(len(visitedNodes),len(open_nodes))

    return None

# This code need to be rebuilt
def possibleMoves(m):
    possibleStates = []
    for car in m.piecesSet:

        #NEED TO CREATE DEEPCOPY BECAUSE PYTHON IS A BAD LANGUAGE

        
        if m.piece_coordinates(car)[0].y == m.piece_coordinates(car)[1].y:

            if m.canMove(car,Coordinates(x=-1,y=0)):
                map2 = copy.deepcopy(m)
                map2.moveWithNoTests(car,Coordinates(x=-1,y=0))
                possibleStates.append([map2.__repr__(),car+"a"])

            if m.canMove(car,Coordinates(x=1,y=0)):
                map3 = copy.deepcopy(m)
                map3.moveWithNoTests(car,Coordinates(x=1,y=0))
                possibleStates.append([map3.__repr__(),car+"d"])
                
        else:
            if m.canMove(car,Coordinates(x=0,y=-1)):
                map2 = copy.deepcopy(m)
                map2.moveWithNoTests(car,Coordinates(x=0,y=-1))
                possibleStates.append([map2.__repr__(),car+"w"])

            if m.canMove(car,Coordinates(x=0,y=1)):
                map2 = copy.deepcopy(m)
                map2.moveWithNoTests(car,Coordinates(x=0,y=1))
                possibleStates.append([map2.__repr__(),car+"s"])



    return possibleStates

""" 
file1 = open('levels.txt', 'r')
Lines = file1.readlines()
j =1
for i in Lines:

    startTime = time.time()
    print(breathsearch(i))
    endTime = time.time()
    print("lever nº " + str(j) + " time is " + str(endTime - startTime) + " seconds")
    j+=1
 """

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py

loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME)) 
