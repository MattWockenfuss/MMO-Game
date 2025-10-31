import asyncio
import utils
import time

from worldclientmanager import WorldClientManager
from playerclientmanager import PlayerClientManager
from dataserverclient import DataServerClient

from terminal import Terminal




class Handler:
    def __init__(self, wcm, pcm, dsc, terminal):
        self.running = True
        self.wcm = wcm
        self.pcm = pcm
        self.dsc = dsc
        self.terminal = terminal

        #active server key is beach-1, and the value would be its codename, IP, Port, and playerCount
        #                           {'beach-1': ['beach', '161.35.137.150', 8004, 4]}
        self.activeServers = {}
        #desiredWorlds key is world name, like beach and value would be 2 (we want to try and have 2 beach worlds)
        self.desiredWorlds = {}


class CommunicationServer:
    def __init__(self):
        self.wcm = WorldClientManager()
        self.pcm = PlayerClientManager()
        self.dsc = DataServerClient()
        self.terminal = Terminal()
        self.handler = Handler(self.wcm, self.pcm, self.dsc, self.terminal)

    async def tick(self):
        RATE = 60
        DT = 1.0 / RATE

        loop = asyncio.get_running_loop()
        next_tick = loop.time()

        while self.handler.running:
            await asyncio.sleep(max(0, next_tick - loop.time()))

            self.wcm.tick(self.handler)
            self.pcm.tick(self.handler)
            self.dsc.tick(self.handler)
            self.terminal.tick(self.handler)

            next_tick += DT
            if loop.time() - next_tick > DT:
                next_tick = loop.time() + DT
    
    async def start(self):
        #first read config
        yml = utils.readYML('config.yml')
    
        self.worldListenAddress = yml.get("worldListenAddress")
        self.worldListenPort = yml.get("worldListenPort")

        self.playerListenAddress = yml.get("playerListenAddress")
        self.playerListenPort = yml.get("playerListenPort")

        self.dataServerAddress = yml.get("dataserverIP")
        self.dataServerPort = yml.get("dataserverPORT")


        print(yml.get('worlds'))

        results = await asyncio.gather(#if one of these stops, they all stop
            self.tick(),
            self.wcm.start(self.worldListenAddress, self.worldListenPort),
            self.pcm.start(self.playerListenAddress, self.playerListenPort),
            self.dsc.start(self.dataServerAddress, self.dataServerPort),
            return_exceptions=True
        )

if __name__ == "__main__":
    asyncio.run(CommunicationServer().start())