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
            
            print(f"You typed: {msg}")
            cmd, *arguments = msg.split()   #the * means take or expand the variable number of positional values
                                            #in this case, a list split on whitespace, the first is set to cmd, the rest are in arguments
            if cmd == "test":
                for arg in arguments:
                    print(f"{arg}")


            if cmd == "reload":
                if len(arguments) != 0:
                    if arguments[0] == "database":
                        #then reload the database
                        handler.CM.readDirectory("configs")
                    elif arguments[0] == "config":
                        #then reload the config file
                        handler.CR.readYML()
            
            if cmd == "tree":
                handler.CM.printDirectories("configs", 1)

            if cmd == "configs":
                #loop through the dictionary, print
                for keys in handler.configs.keys():
                    print(keys)
                    for value in handler.configs[keys]:
                        print(f"-{value}")

            if cmd == "exit" or cmd == "shutdown":
                print("Shutting Down Server!")
                handler.shutdown.set()



        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())


            