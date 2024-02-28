#!/usr/bin/env python

import asyncio

import websockets
import secrets
import json

connected = set()

users_connected = {"key": dict()}


async def handler(websocket):
    while True:
        try:
            async for message in websocket:    
                data = json.loads(message)
                action = data.get("action")
                
                match action:
                    case "connect":        
                        await handle_connect(websocket)
                    case "start":
                        await handle_start(data, websocket)
                    case "join":
                        await handle_join(data, websocket)
                    case "play":
                        await handle_change_message(data, websocket)
                
        except websockets.ConnectionClosedOK:
           connected.discard(websocket)


async def handle_connect(websocket):
    try:
        if(websocket not in connected):
            connected.add(websocket)
            websockets.broadcast(connected, "New user has joined")
    finally: 
        pass


async def handle_start(data,websocket):
    try:
        origen = data.get('user')
        join_key = secrets.token_urlsafe(12)
        users_connected[join_key] = {origen: websocket}
        await websocket.send(json.dumps({"key": join_key}))
    finally: 
        pass
    
async def handle_join(data, websocket):
    try:
        join_key = data.get('key')
        origen = data.get('user')
        
        if(join_key in users_connected):
            users_connected[join_key][origen] = websocket
            
            set_data = set(users_connected[join_key].values())
            websockets.broadcast(set_data, "you are connected with a user")
        else:
            await websocket.send(json.dumps({"error": "join key not valid"}))
    finally: 
        pass

async def handle_change_message(data, websocket):
    try:
        join_key = data.get('key')
        origen = data.get('user')
        destination = data.get('destination')
        message = data.get('message')
        
        if(join_key in users_connected):
            information = json.dumps({
            "from": origen,
            "message": message
            })
            
            print()
            print(information)
            print()
            
            await users_connected[join_key][destination].send(information)
        else:
            await websocket.send(json.dumps({"error": "join key not valid"}))
    finally: 
        pass

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())