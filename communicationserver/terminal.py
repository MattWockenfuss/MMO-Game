import asyncio
import os


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

            cmd, *args = msg.split()
            #print(f"/{cmd} with args:[{args}]")

            if cmd == "help":
                print(f"worlds")
                print(f"\tPrints Out the current list of worlds!")
                print(f"desired")
                print(f"\tPrints out the servers set in the config that are desired and their counts")
                print(f"clear ('cls')")
                print(f"\tClears the screen")


            if cmd == 'desired':
                print(handler.wcm.desiredWorlds)

            if cmd == 'players':
                for wUUID, worldserver in  handler.wcm.worldclients.items():
                    print(f"[{wUUID}-{worldserver.getIPString()}] {worldserver.nameID:12} has {worldserver.playerCount} player(s)")
                    for pUUID, playername in worldserver.players.items():
                        print(f"  - [{pUUID}] {playername}")

            if cmd == 'worlds':
                #then we want to list all of the worlds, their IPs, their type and player count, 
                for UUID, worldserver in handler.wcm.worldclients.items():
                    print(f"[{UUID}-{worldserver.getIPString()}] {worldserver.nameID:12} Desired: {handler.wcm.desiredWorlds[worldserver.type]} {worldserver.playerCount} players ")
                print(f"Players connect to a '{handler.wcm.defaultServer}' server on login!")

            if cmd == "cls" or cmd == "clear":
                if os.name == "nt":
                    os.system("cls")    #works on windows
                else:
                    os.system("clear")  #works on everything else


            if cmd == 'pingDS':
                dx = {
                        "username": "Johnny", 
                        "password": "12309841",
                        "UUID": "KKKK"
                    }
                handler.dsc.sendMsg("AUTH_REQ", dx)



        
        # Schedule new input task if none running
        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())