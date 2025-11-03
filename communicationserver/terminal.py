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
            print(f"/{cmd} with args:[{args}]")

            if cmd == 'desired':
                print(handler.wcm.desiredWorlds)



        
        # Schedule new input task if none running
        if self.task is None:
            self.task = asyncio.create_task(self.getTerminalInput())