#This should accept incoming and outgoing packets from any server, addressed to another server
#Next steps:
#


import asyncio

class CommServer:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.clients = {}  # key: server name, value: writer

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr}")

        # First packet should identify the server type
        data = await reader.read(100)
        server_type = data.decode().strip()
        self.clients[server_type] = writer
        print(f"Registered {server_type} server")

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                #Packet format: "target_server|payload"
                msg = data.decode()
                # Validate message structure
                parts = msg.split('|')

                if len(parts) != 2:
                    print(f"Malformed packet (wrong number of parts): {msg}")
                    return  # Or continue to next loop iteration

                target, payload = parts

                if not target or not payload: #if one part of the message is missing
                    print(f"Malformed packet (empty target or payload): {msg}")
                    return

                # If the message is formatted correctly, route to valid client
                if target in self.clients:
                    try:
                        self.clients[target].write(payload.encode())
                        await asyncio.wait_for(self.clients[target].drain(), timeout=5)
                        print(f"Forwarded packet to {target}: {payload}")
                    except asyncio.TimeoutError:
                        print(f"Timeout while sending to {target}")
                else:
                    print(f"Unknown target server: {target}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f"Closing connection from {addr}")
            writer.close()
            await writer.wait_closed()
            # Remove client
            for key, val in list(self.clients.items()):
                if val == writer:
                    del self.clients[key]

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"CommServer running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(CommServer().start())