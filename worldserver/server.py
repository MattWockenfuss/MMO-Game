"""
worldserver/server.py

Main server module for the MMO World Server component.

Responsibilities:
- Initialize and manage core game world subsystems including world state, entity management,
  client socket communication, data server communication, and terminal interface.
- Implement the main async event loop running at 60 ticks per second to drive game logic updates.
- Provide benchmarking functionality to monitor server tick performance in real-time.
- Coordinate startup and graceful shutdown of subsystems.

Dependencies:
- config: Configuration reader for server settings.
- dataserverclient: Manages communication with the data server.
- clientsocketmanager: Manages client connections and messaging.
- world: Represents the game world state and logic.
- entitymanager: Manages game entities and their states.
- terminal: Provides a terminal interface for server commands and debugging.
- asyncio and time libraries for async event loop and performance timing.
"""


from config import ConfigReader
from dataserverclient import DataServerClient
from commsserverclient import CommsServerClient
from clientsocketmanager import ClientSocketManager
from world import World
from entitymanager import EntityManager
from terminal import Terminal

import time

'''
Websockets: 
    https://websockets.readthedocs.io/en/stable/
Asyncio
    https://docs.python.org/3/contents.html


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
    """
    Container for all main server subsystems and shared state.
    Holds references to DataServerClient, ClientSocketManager,
    World, EntityManager, Terminal, and Benchmark instances.
    Controls the running state of the server loop.
    """
    def __init__(self):
        self.running = True
        self.dsc = None
        self.csm = None
        self.csc = None
        self.world = None
        self.em = None
        self.terminal = None
        self.benchmark = None

class Benchmark:
    """
    Measures and reports ticks per second (TPS) and frame durations
    for performance monitoring during server runtime.
    """
    def __init__(self):
        self.active = False

    """
        Start benchmarking session.

        Args:
            nowTime (float): Current time from event loop.
            intervalTime (float): Interval between reporting performance stats.
            totalTime (float): Total duration to run benchmarking.
    """
    def start(self, nowTime, intervalTime, totalTime): #The Asterisk means that after the asterisk, no longer excepts positional arguments

        self.active = True

        self.interval_frame_times = []
        self.total_frame_times = []

        self.intervalTime = intervalTime
        self.totalTime = totalTime
        self.nextEmit = nowTime + intervalTime
        self.endTime = nowTime + totalTime
        print(f"{nowTime} => {self.nextEmit} {self.endTime}")


    """
        Record the duration of a single frame (tick) and print stats
        at specified intervals and at the end of the benchmarking period.

        Args:
            now (float): Current time from event loop.
            duration_ms (float): Duration of last frame in milliseconds.
    """
    def record(self, now, duration_ms: float):

        
        if not self.active: return
        self.interval_frame_times.append(duration_ms)
        self.total_frame_times.append(duration_ms)

        if now >= self.nextEmit:
            #print(f"Recording!")
            fps = len(self.interval_frame_times) / self.intervalTime
            avg = sum(self.interval_frame_times) / len(self.interval_frame_times)
            low = min(self.interval_frame_times)
            high = max(self.interval_frame_times)

            print(f"[BENCHMARK] TPS: {fps:.2f} Avg: {avg:.2f} ms Max: {high:.2f} ms Min: {low:.2f} ms")

            self.interval_frame_times.clear()
            self.nextEmit += self.intervalTime

        if now >= self.endTime:
            #then this is the last interval
            fps = len(self.total_frame_times) / self.totalTime
            avg = sum(self.total_frame_times) / len(self.total_frame_times)
            low = min(self.total_frame_times)
            high = max(self.total_frame_times)
        
            print(f"[BENCHMARK] FINAL TPS: {fps:.2f} Avg: {avg:.2f} ms Max: {high:.2f} ms Min: {low:.2f} ms")


            self.active = False
            self.interval_frame_times.clear()
            self.total_frame_times.clear()




class WorldServer:
    """
    Main world server class coordinating the MMO game server operation.
    Initializes all subsystems and runs the async main loop to process ticks.
    """
    def __init__(self):
        self.handler = Handler()

        self.world = World()
        self.em = EntityManager()
        self.dsc = DataServerClient()
        self.csc = CommsServerClient()
        self.csm = ClientSocketManager(self.handler)
        self.terminal = Terminal()
        self.benchmark = Benchmark()
        
        self.handler.world = self.world
        self.handler.em = self.em
        self.handler.dsc = self.dsc
        self.handler.csc = self.csc
        self.handler.csm = self.csm
        self.handler.terminal = self.terminal
        self.handler.benchmark = self.benchmark

        self.handler.em.handler = self.handler
        
    async def tick(self):

        RATE = 60
        DT = 1.0 / RATE

        loop = asyncio.get_running_loop()
        next_tick = loop.time()
        
        while self.csm.IP is None or self.csm.Port is None or getattr(self.csc, "ws", None) is None:
            print(f"Waiting for {self.csm.IP} to not be None!")
            await asyncio.sleep(0.01)



        d = {
            'port': f'{self.csm.Port}'
        }
        self.csc.sendMsg('register', d)


        while self.handler.running:
            await asyncio.sleep(max(0, next_tick - loop.time()))
            frame_start = time.perf_counter()

            self.dsc.tick(self.handler)
            self.csc.tick(self.handler)
            self.csm.tick(self.handler)
            self.world.tick(self.handler)
            self.em.tick(self.handler)
            self.terminal.tick(self.handler)

            frame_dur = (time.perf_counter() - frame_start) * 1000.0
            self.benchmark.record(loop.time(), frame_dur)



            next_tick += DT
            if loop.time() - next_tick > DT:
                next_tick = loop.time() + DT
            



        await self.dsc.stop(code=1000, reason="Shutdown!")
        await self.csm.stop()


    async def start(self):
        """
        Starts the world server by reading configuration,
        then concurrently starting the main tick loop,
        data server client, and client socket manager.
        """
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
        print(f"OPENING SOCKETS IN START METHOD!!!!")

        pingInterval = 20
        pingTimeout = 20


        await asyncio.gather(#if one of these stops, they all stop
            self.tick(),
            self.dsc.start(self.cf.get("DataServer-IP"), self.cf.get("DataServer-Port")),
            self.csc.start(self.cf.get("CommsServer-IP"), self.cf.get("CommsServer-Port")),
            self.csm.start(self.cf.get("listenAddress"), 0, pingInterval, pingTimeout)
        )


    

ws = WorldServer()
asyncio.run(ws.start())