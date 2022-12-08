import asyncio
import copy
import getpass
import imp
from importlib.resources import path
import json
import math
from mimetypes import common_types
import os
from re import search
import time
from tracemalloc import start
from my_common import Coordinates, Map
from commonMethods import breathsearch, AStar
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
        counter = 0
        
        
        
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                

                if state.get('level') != level:
                    level = state.get('level')
                    moves = ''
                    currentlySearching = False
                    mapa = Map(state.get("grid"))
                    mapaString = state.get("grid").split(" ")[1]
                    counter = 0


                if not currentlySearching:
                    currentlySearching = True
                    moves =  AStar(state.get("grid"))


                if mapaString != state.get("grid").split(" ")[1]:
                    newMapa = Map(state.get("grid"))
                    if counter == 30:

                        currentlySearching = True
                        moves =  AStar(state.get("grid"))
                        counter = 0

                    # Only send the crazy cars backwards if it is faster than calculating a new solution
                    # For this is i use the ammount of possible states
                    if int(state.get("grid").split(" ")[2]) > 2000:

                        try: # I use a try only if something goes wrong calculating the crazy cars
                            crazyMoves = calculateCrazyMoves(newMapa,mapa)
                            mapa = Map(state.get("grid"))
                            moves = crazyMoves + moves
                            mapaString = state.get("grid").split(" ")[1]
                            counter +=1
                        except: # recalculates a solution
                            currentlySearching = True
                            print("recalculates from crazyMoves currentlySearching")
                            moves =  AStar(state.get("grid"))
                            mapaString = state.get("grid").split(" ")[1]
                            mapa = Map(state.get("grid"))
                    else:
                        counter +=1
                        currentlySearching = True
                        print("recalculates from crazyMoves currentlySearching",counter)
                        moves =  AStar(state.get("grid"))
                        mapaString = state.get("grid").split(" ")[1]
                        mapa = Map(state.get("grid"))





            
                #if moves == "":
                #    continue
                


                    
                    
                # do the move
                try:
                    mapaString, moves, key = getNextMove(moves,state.get("cursor"),mapa,state.get("selected"),mapaString)

                except: # recalculates a solution
                    currentlySearching = True
                    moves =  AStar(state.get("grid"))
                    mapaString = state.get("grid")
                    mapa = Map(state.get("grid"))
                    continue

                await websocket.send(json.dumps({"cmd": "key", "key": key})) 

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


def calculateCrazyMoves(newMap,oldMapa):
    crazy_moves = ""
    grid_str = oldMapa.__repr__().split(" ")[1]
    new_grid_str = newMap.__repr__().split(" ")[1]

    
    print("crazies ---------------------------------")

    while (grid_str != new_grid_str):
        crazy_car = None
        positive = 0


        for i in range(len(grid_str)):
            old_char = grid_str[i]
            new_char = new_grid_str[i]
            # Gets the odd character
            if new_char != old_char:
                crazy_car = old_char if old_char != 'o' else new_char
                positive = -1 if old_char != 'o' else 1
                break
            

        if oldMapa.piece_coordinates(crazy_car)[0].y == oldMapa.piece_coordinates(crazy_car)[1].y:
            print("horizontal")
            if positive == -1:
                crazy_moves = crazy_moves + crazy_car+"a"
                print(crazy_car,letterToCoords("a"))
                newMap.move(crazy_car,letterToCoords("a")) #moves car in the map Object
                
            else:
                crazy_moves = crazy_moves + crazy_car+"d"
                print(crazy_car,letterToCoords("d"))
                newMap.move(crazy_car,letterToCoords("d")) #moves car in the map Object


        else:

            if positive == -1:
                crazy_moves = crazy_moves + crazy_car+"w"
                print(crazy_car,letterToCoords("w"))
                newMap.move(crazy_car,letterToCoords("w")) #moves car in the map Object
            else:
                crazy_moves = crazy_moves + crazy_car+"s"
                print(crazy_car,letterToCoords("s"))
                newMap.move(crazy_car,letterToCoords("s")) #moves car in the map Object



        grid_str = oldMapa.__repr__().split(" ")[1]
        new_grid_str = newMap.__repr__().split(" ")[1]




    return crazy_moves

def getNextMove(moves,cursor,mapa,selected,mapaString):
    
    cursorPos = Coordinates(cursor[0],cursor[1])
    #If a car is selected
    if selected != "":

        # if it is the correct car
        if selected == moves[0]:


            key = moves[1] #selects the move

            mapa.move(moves[0],letterToCoords(moves[1])) #moves car in the map Object

            moves =  moves[2:]  #removes the move from the grid
            

            # To make this a bit faster in checking the Crazy Drivers
            # This will only change the MapaString variable
            # using the Map.__repr_ method takes O(n)
            # maybe there is a better solution, Problem for future me

            #Future me here, im not doing any of this, its python, who care about time complexities

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
  







# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py

loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME)) 

