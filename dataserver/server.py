#this is a comment in python
#So Tiles need to be loaded before worlds
#https://pyyaml.org/wiki/PyYAMLDocumentation
#https://websockets.readthedocs.io/en/stable/intro/tutorial1.html#download-the-starter-kit

import json
import utils
import asyncio

from config import ConfigManager, ConfigReader
from terminal import Terminal
from worldclientmanager import WorldClientManager


class Handler:
    def __init__(self, configs, worldclientmanager, CM, CR):
        self.shutdown = asyncio.Event()
        self.configs = configs
        self.wcm = worldclientmanager
        self.CM = CM
        self.CR = CR


class DataServer:
    def __init__(self):
        self.wcm = WorldClientManager()
        self.terminal = Terminal()

        self.CR = ConfigReader("data-server.yml")
        self.CR.readYML()

        self.CM = ConfigManager()
        self.CM.readDirectory("configs")
        self.CM.printDirectories('configs', 1)

        self.handler = Handler(self.CM.database, self.wcm, self.CM, self.CR)


     
        
    async def tick(self):
        while not self.handler.shutdown.is_set():
            if self.handler.shutdown.is_set():
                break
            await asyncio.sleep(0.5)
            #print("Tick Method!")
            self.terminal.tick(self.handler)
        await self.wcm.stop()
        


    async def start(self):
        for item in self.CM.database["worlds"]:
            utils.loadMapImage(item, self.CM.database)
        
        
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.tick())
            tg.create_task(self.wcm.start(self.CR.get("listenAddress"), self.CR.get("myPort"), self.handler))

                
if __name__ == "__main__":
    ds = DataServer()
    asyncio.run(ds.start())
    