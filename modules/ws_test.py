import asyncio
import websockets
import time

async def hello():
    uri = "ws://localhost:7181/logs"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"logfile": "/Users/xianglei/Develop/Idea/bunny/a.log"}')
    while True:
        try:
            response = await websocket.recv()
            print(f"Received: {response}")
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(1)  # wait for 1 second before trying to reconnect

asyncio.run(hello())
