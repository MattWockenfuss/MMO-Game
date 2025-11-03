"""
worldserver/terminal.py

Terminal input handler for the MMO World Server.

Responsibilities:
- Provides an async interface to receive text commands from the server terminal.
- Parses commands entered at the terminal and executes corresponding server actions.
- Supports commands for server control, player management, benchmarking, querying game state, and terminal utility functions (e.g., clear screen).
- Runs in a tick function that continuously checks for new input and processes it asynchronously.

Dependencies:
- asyncio: For asynchronous input reading and task scheduling.
- os: To execute terminal commands like clearing the screen.
"""

import asyncio
import os

'''
This module processes terminal commands asynchronously.
Commands allow interaction with the worldserver subsystem to query state or control players.

Example commands:
- help: Prints a list of available commands and their usage.
- desert: Requests world data for "The Desert" from the dataserver.
- benchmark <interval> <total>: Runs a TPS benchmarking session over a specified duration.
- players: Lists all currently connected players.
- entities: Lists all entities present on the server.
- herds: Lists enemy herds or details for a named herd.
- sockets: Lists all connected client sockets.
- kick <name>: Kicks a player by name.
- kickall: Kicks all connected players.
- clear or cls: Clears the terminal screen.
- exit: Shuts down the server loop.
'''

class Terminal:
    """
    Terminal input handler class.

    Manages asynchronous reading of server console input,
    parsing commands and executing corresponding server-side actions.
    """
    def __init__(self):
        self.task = None

    async def getTerminalInput(self):
        """
        Asynchronously reads a line of input from the terminal
        in a non-blocking manner using an executor.

        Returns:
            str: The input string entered by the user.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "'help' for commands, or 'exit' to quit\n")

    def tick(self, handler):
        """
        Called periodically by the server main loop to process terminal input.

        If an input task is completed, retrieve and parse the command,
        then perform the requested action by interacting with the handler subsystems.

        Args:
            handler (Handler): The main server handler containing subsystem references.
        """
        if self.task and self.task.done():

            msg = None
            try:
                msg = self.task.result()
            except Exception as e:
                print(f"Failed on Input at CMD Line: {e}")
            
            self.task = None
            if not msg: return

            #   the * means take or expand the variable number of positional values
            #   in this case, a list split on whitespace, the first is set to cmd, the rest are in arguments
            cmd, *args = msg.split()

            if cmd == "help":
                print(f"desert")
                print(f"\tSends a world request to the dataserver for desert!")
                print(f"players")
                print(f"\tlists all active players connected")
                print(f"entities")
                print(f"\tlists all entities")
                print(f"herds")
                print(f"\tlists all herds")
                print(f"benchmark <interval> <total>")
                print(f"\tRuns a TPS benchmark, printing at <interval> seconds for <total> seconds")
                print(f"sockets")
                print(f"\tlist all the connected sockets (unauthed players)")
                print(f"kick <name>")
                print(f"\tKicks the specified player by name")
                print(f"kickall")
                print(f"\tKicks all connected players")
                print(f"clear ('cls')")
                print(f"\tClears the screen")


            if cmd == "benchmark":
                if len(args) < 2:
                    print(f"Not Enough Arguments! Usage: 'benchmark <interval> <total>'")
                if handler.benchmark.active:
                    print(f"Benchmark Already active!")

                interval = float(args[0])
                total = float(args[1])

                print(f"[BENCHMARK] Starting benchmarking at {interval} second intervals over {total} seconds")
                handler.benchmark.start(asyncio.get_running_loop().time(), interval, total)
            
            
            if cmd == "players":
                if len(handler.csm.players.items()) == 0:
                    print(f"There are no players on the server!")
                else:
                    print(f"logged in: {len(handler.csm.players)} players")
                    for sessID, player in list(handler.csm.players.items()):
                        print(" " * 4, end="")
                        print(f"{sessID} {player.username} ", end="")
                        print(f"{player.userdata} ")

            if cmd == "entities":
                if(len(handler.em.items) == 0):
                    print(f"There are no entities on the server!?!?!?!")
                else:
                    for entity in handler.em.items:
                        print(f"\t{entity.UUID} {entity.type} ({entity.x},{entity.y})")
            
            if cmd == "herds":
                if len(args) == 0:
                    for herd in handler.world.enemyHerds:
                        print(f"{herd.herdName} ({herd.coords[0]},{herd.coords[1]}), Count: {herd.currentCount} Cooldown: {herd.cooldownTimer} in {herd.cooldown}")
                else:
                    for herd in handler.world.enemyHerds:
                        if herd.herdName == args[0].lower():
                            herd.printInfo()




            if cmd == "sockets":
                if len(handler.csm.clients.items()) == 0:
                    print(f"There are no clients on the server!")
                else:
                    print(f"logged in: {len(handler.csm.clients)} clients")
                    for sessID, client in list(handler.csm.clients.items()):
                        print(" " * 4, end="")
                        print(f"{sessID} {client} ")

            if cmd == "kick":
                if len(args) == 0:
                    print(f"kick <name>")
                else:
                    #okay so args[0] is our players name
                    for sessID, player in list(handler.csm.players.items()):
                        if args[0] == player.username:
                            #kick them
                            print(f"Kicked {player.username}")
                            handler.csm.kick(sessID, code = 1000, reason = "Kicked by Console!")
                            
            
            if cmd == "kickall":
                #then we want to kickall players
                for sessID, player in list(handler.csm.players.items()):
                    handler.csm.kick(sessID, code = 1000, reason = "Kicked by Console!")


            if cmd == "cls" or cmd == "clear":
                if os.name == "nt":
                    os.system("cls")    #works on windows
                else:
                    os.system("clear")  #works on everything else


            if cmd == "exit":
                handler.running = False
                print(f"Closing")


        # Schedule new input task if none running
        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())


            