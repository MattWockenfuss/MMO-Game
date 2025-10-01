#this is a dummy client, be able to send data to web socket

import asyncio
import websockets

async def run_client():
    uri = "ws://localhost:8002"
    async with websockets.connect(uri) as ws:

        while True:
            msg = input("Awaiting your input to send\n")

            if msg == "exit":
                break

            await ws.send(msg)
            reply = await ws.recv()
            print(f"[Server] -> {reply}")


if __name__ == "__main__":
    asyncio.run(run_client())


