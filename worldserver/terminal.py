import asyncio

'''
    This is going to represent the piece of the code that is the input handler for our terminal, we will be able to parse commands
    and act accordingly depending on the command, maybe even add arguments, or an argument for that matter

'''

class Terminal:
    def __init__(self):
        self.task = None

    async def getTerminalInput(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "Please type a msg (or exit to quit)\n")

    def tick(self, handler):

        if self.task and self.task.done():
            try:
                msg = self.task.result()
            except:
                print(f"Failed on Input at CMD Line")
                msg = None

            self.task = None
            

            #print(f"You typed: {msg}")

            cmd, *args = msg.split()

            if cmd == "a":
                handler.dsc.sendMsg("test", "Hello Data Server!")

            if cmd == "b":
                handler.dsc.sendMsg("world",{'World-Name':'Big Forest'})
            
            if cmd == "c":
                handler.dsc.sendMsg("enemy", {'Enemy':'Forest'})

            if cmd == "d":
                handler.dsc.sendMsg("world", {'Enemy':'Skeleton'})
            
            if cmd == "e":
                handler.dsc.sendMsg("world", {'World-Name':'Test World'})

            if cmd == "f":
                handler.dsc.sendMsg("world", {'World-Name':'Caves'})
            
            


            if cmd == "players":
                if len(handler.csm.players.items()) == 0:
                    print(f"There are no players on the server!")
                else:
                    print(f"logged in: {len(handler.csm.players)} players")
                    for key, player in list(handler.csm.players.items()):
                        print(" " * 4, end="")
                        print(f"{key} {player.name} ", end="")
                        print(f"{player.data} ")

            if cmd == "sockets":
                if len(handler.csm.clients.items()) == 0:
                    print(f"There are no clients on the server!")
                else:
                    print(f"logged in: {len(handler.csm.clients)} clients")
                    for key, client in list(handler.csm.clients.items()):
                        print(" " * 4, end="")
                        print(f"{key} {client} ")

            if cmd == "kick":
                if len(args) == 0:
                    print(f"kick <name>")
                else:
                    #okay so args[0] is our players name
                    for sessID, player in list(handler.csm.players.items()):
                        #print("Hello")
                        #print(f"Kicking {args[0]} =? {sessID} and {player.player.username}")
                        if args[0] == player.player.username:
                            #kick them
                            handler.csm.kickClient(player.player.username, code=1004, reason="Kicked by Console!")


            if cmd == "exit":
                handler.running = False
                print(f"Closing")



        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())


            