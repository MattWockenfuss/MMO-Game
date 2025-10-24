import asyncio
import os

'''
    This is going to represent the piece of the code that is the input handler for our terminal, we will be able to parse commands
    and act accordingly depending on the command, maybe even add arguments, or an argument for that matter

'''

class Terminal:
    def __init__(self):
        self.task = None

    async def getTerminalInput(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "'help' for commands, or 'exit' to quit\n")

    def tick(self, handler):

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


            if cmd == "desert":
                handler.dsc.sendMsg("world", {'World-Name':'The Desert'})

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



        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())


            