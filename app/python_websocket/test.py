import asyncio
import websockets
import json

async def send_message(user_id, destination, message):
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        data = {
            "user": user_id,
            "destination": destination,
            "message": message
        }
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)

# Test sending messages to users
async def test():
    await send_message("dercio", "amaro", "como estas")
    await send_message("amaro", "dercio", "estoy bien, gracias")
    await send_message("dercio", "noone", "message to non-existent user")

if __name__ == "__main__":
    asyncio.run(test())
