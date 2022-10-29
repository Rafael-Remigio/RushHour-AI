"""Example client."""
import asyncio
import copy
import getpass
import imp
import json
from mimetypes import common_types
import os
from re import search
from common import Coordinates, Map
# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets



async def agent_loop(server_address="localhost:8085", agent_name="mr_Robot"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))


        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                print(state)
                print(state.get("cursor"))
                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            key = "w"
                        elif event.key == pygame.K_LEFT:
                            key = "a"
                        elif event.key == pygame.K_DOWN:
                            key = "s"
                        elif event.key == pygame.K_RIGHT:
                            key = "d"
                        elif event.key == pygame.K_SPACE:
                            key = " "

                        elif event.key == pygame.K_d:
                            import pprint

                            pprint.pprint(state)

                        await websocket.send(
                            json.dumps({"cmd": "key", "key": key})
                        )  # send key command to server - you must implement this send in the AI agent
                        break
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

def search(startState):
    open_nodes = [startState]
    visitedNodes = set()
    while open_nodes != []:
            node = open_nodes.pop(0)
            mapa = Map(node)
            if mapa.test_win():
                solution = node
                print(mapa.grid)
                return solution
            for a in possibleMoves(mapa):
                print(a)
                if not visitedNodes.__contains__(a):
                    open_nodes.append(a)
            visitedNodes.add(node)
            print("sdasdasdasds")


    return None


def possibleMoves(m):
    possibleStates = []
    print(m.pieces)
    for i in range(m.pieces):
        car = chr(65+i)
        map2 = copy.deepcopy(m)
        map3 = copy.deepcopy(m)
        print(m.piece_coordinates(car))
        if m.piece_coordinates(car)[0].y == m.piece_coordinates(car)[1].y:
            try:
                map2.move(car,Coordinates(x=-1,y=0))
                possibleStates.append(map2.__repr__())

            except:
                map2 = m
            try:
                map3.move(car,Coordinates(x=1,y=0))
                possibleStates.append(map3.__repr__())

            except:
                map3 = m

        else:
            try:
                map2.move(car,Coordinates(x=0,y=-1))
                possibleStates.append(map2.__repr__())

            except:                
                map2 = m

            try:
                map3.move(car,Coordinates(x=0,y=1))
                possibleStates.append(map3.__repr__())

            except:
                map3 = m

    return possibleStates

m = Map("02 ooooooooBoooAABooooooooooooooooooooo 21")
print(m.pieces)
for i in m.grid:
    print(i)
#print(m.coordinates)
#print(m.__repr__())
#print(m.coordinates)
#print(m.piece_coordinates("A"))
#print(m.__repr__())
#print(m.pieces)
#print(m.grid)
print(possibleMoves(m))

print()
print(search("03 ooBoooooBooCAABooCoooooooooooooooooo 62"))

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
""" 
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8085")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME)) 
"""
