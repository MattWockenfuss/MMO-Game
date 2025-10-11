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
        return await loop.run_in_executor(None, input, "Please type 'help' for commands, or 'exit' to quit\n")

    def tick(self, handler):
        if self.task and self.task.done():

            try:
                msg = self.task.result()
            except:
                print(f"Failed on Input at CMD Line")
                msg = None

            self.task = None
            
            cmd, *arguments = msg.split()   #the * means take or expand the variable number of positional values
                                            #in this case, a list split on whitespace, the first is set to cmd, the rest are in arguments
            
            if cmd == "help":
                print(f"test <args>")
                print(f"\tTest command, prints out args")
                print(f"reload <database / configs>")
                print(f"\tReloads and Rereads Appropriate config files. Database contains the entities, tiles, worlds, etc..., while configs is the dataserver's config file")
                print(f"tree")
                print(f"\tPrints a tree of the current directory.")
                print(f"configs")
                print(f"\tPrints out the entire stored dictionary, skips world data")
                print(f"clear ('cls')")
                print(f"\tClears the screen")
            
            if cmd == "test":
                for arg in arguments:
                    print(f"{arg}")


            if cmd == "reload":
                if len(arguments) != 0:
                    if arguments[0] == "database":
                        #then reload the database
                        handler.CM.readDirectory("configs")
                        handler.configs = handler.CM.database
                    elif arguments[0] == "config":
                        #then reload the config file
                        handler.CR.readYML()
                        print(f"Reloaded Config File!")
            
            if cmd == "tree":
                handler.CM.printDirectories("configs", 1)

            if cmd == "configs":
                #loop through the dictionary, print
                for keys in handler.configs.keys():
                    print(keys)
                    for value in handler.configs[keys]:
                        #so each one of these values is a thing stored, could be a world, etc...
                        if keys == "worlds":
                            print("{", end="")
                            for tag in value:
                                if tag == "world-data":
                                    print(f"{tag}: ..., ", end="")
                                    continue
                                print(f"{tag}: {value[tag]}, ", end="")
                            print("}")
                        else:
                            print(f"-{value}")
            if cmd == "tiles":
                #then print the tiles dictionary
                for value in handler.configs["tiles"]:
                    print(f"{value}")

            if cmd == "cls" or cmd == "clear":
                if os.name == "nt":
                    os.system("cls")    #works on windows
                else:
                    os.system("clear")  #works on everything else

            if cmd == "exit" or cmd == "shutdown":
                print("Shutting Down Server!")
                handler.shutdown.set()



        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())


            