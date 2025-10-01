import asyncio, json, sys, time
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

URI = "ws://127.0.0.1:8001"

async def reader(ws):
    try:
        async for msg in ws:
            print("<-", msg)
    except (ConnectionClosedOK, ConnectionClosedError) as e:
        print(f"[reader] closed: {getattr(e, 'code', '?')} {getattr(e, 'reason', e)}")

async def heartbeat(ws, interval=15):
    # App-level heartbeat (separate from protocol ping/pong)
    try:
        while True:
            await asyncio.sleep(interval)
            await ws.send(json.dumps({"type": "ping", "t": time.time()}))
            # You can also await ws.ping() if you want protocol-level pings from client.
    except (ConnectionClosedOK, ConnectionClosedError):
        pass

async def user_input(ws):
    # Don't use input(); it blocks the event loop.
    loop = asyncio.get_running_loop()
    try:
        while True:
            line = await asyncio.to_thread(sys.stdin.readline)
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            # If you want to send JSON, validate/format here:
            try:
                payload = json.loads(line)  # allow typing raw JSON lines
            except json.JSONDecodeError:
                payload = {"type": "chat", "message": line}
            await ws.send(json.dumps(payload))
            print("->", payload)
    except (ConnectionClosedOK, ConnectionClosedError):
        pass

async def run_client():
    backoff = 1
    while True:
        try:
            async with websockets.connect(URI, ping_interval=30, ping_timeout=30, close_timeout=5, max_queue=32,) as ws:
                print("[client] connected")
                backoff = 1  # reset backoff on successful connect
                # Race three tasks: reader, heartbeat, and console sender
                await asyncio.gather( #okay so .gather waits for all of the functions to run
                    reader(ws),
                    heartbeat(ws, 15),
                    user_input(ws),
                )
        except Exception as e:
            print(f"[client] connect error: {e}. Reconnecting in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30)  # capped exponential backoff




if __name__ == "__main__":
    asyncio.run(run_client())
