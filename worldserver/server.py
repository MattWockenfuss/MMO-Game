from config import ConfigReader
from dataserverclient import DataServerClient
from clientsocketmanager import ClientSocketManager
from world import World
from entitymanager import EntityManager
from terminal import Terminal


'''
Websockets: 
    https://websockets.readthedocs.io/en/stable/
Asyncio
    https://docs.python.org/3/contents.html

✅ added terminal so nonblock
✅ added queues to clientsockets
✅ Move Terminal tick to main tick method


Todo:
    switch data server to Object Oriented
    Change Data Server to use Task Groups Not .gather
    Add tick Method to Data Server
    Add Queues to Data Server
    Add terminal to data server
    Add handler to DSPacketHandler

    Define a packet library and way to transport data


'''


import asyncio

class Handler:
    def __init__(self, dsc, csm, world, em, terminal):
        self.running = True
        self.dsc = dsc
        self.csm = csm
        self.world = world
        self.em = em
        self.terminal = terminal






class WorldServer:
    def __init__(self):
        self.world = World()
        self.em = EntityManager()
        self.dsc = DataServerClient()
        self.csm = ClientSocketManager()
        self.terminal = Terminal()
        self.handler = Handler(self.dsc, self.csm, self.world, self.em, self.terminal)
        

    async def tick(self):
        while self.handler.running:
            await asyncio.sleep(1 / 60)
            self.dsc.tick(self.handler)
            self.csm.tick(self.handler)
            self.world.tick(self.handler)
            self.em.tick(self.handler)
            self.terminal.tick(self.handler)
        print("before")
        await self.dsc.stop(code=1000,reason="Shutdown!")
        print("middle?")
        await self.csm.stop()
        print("Done?")



    async def start(self):
        self.cf = ConfigReader("world-server.yml")
        self.cf.readYML()
        self.cf.printConfigData()
        '''
                    self.tick()
                process all of our inbound msgs,
                msg could be move packet, could be disconnnect, could be kill, could be 
                tick the world, tick the entities
                 entities update their actions
                 add new data to outbound queues, entity positions, entity dealing damage, player moving, etc...
        
        '''
        results = await asyncio.gather(#if one of these stops, they all stop
            self.tick(),
            self.dsc.start(self.cf.get("DataServer-IP"), self.cf.get("DataServer-Port")),
            self.csm.start(self.cf.get("listenAddress"), self.cf.get("myPort"), self.cf.get("pingInterval"), self.cf.get("pingTimeout")),
            return_exceptions=True
        )

        print(results)
        print("Closing Server!")


    

ws = WorldServer()
asyncio.run(ws.start())