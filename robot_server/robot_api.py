#!/usr/bin/env python3
"""
Minimal FastAPI server for robot communication over HTTPS/WebSockets with self-signed certificates
"""
import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

# Create FastAPI app
app = FastAPI(title="Robot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for certificates
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "certs")

# Certificate paths
CERT_FILE = os.path.join(CERT_DIR, "server.crt")
KEY_FILE = os.path.join(CERT_DIR, "server.key")

# Sample robot data
robot_data = {
    "name": "Test Robot",
    "status": "online",
    "battery": 87,
    "position": {"x": 10, "y": 20, "z": 0},
    "sensors": {
        "temperature": 25.6,
        "humidity": 40.2,
        "pressure": 1013.2
    }
}

# REST API endpoints
@app.get("/")
async def root():
    return {"message": "Robot API is online"}

@app.get("/api/status")
async def status():
    # Update some values to simulate changing data
    robot_data["battery"] = max(0, min(100, robot_data["battery"] + random.uniform(-1, 0.5)))
    robot_data["sensors"]["temperature"] = round(robot_data["sensors"]["temperature"] + random.uniform(-0.2, 0.2), 1)
    
    return {
        "status": "online",
        "secure": True,
        "protocol": "https",
        "timestamp": datetime.now().isoformat(),
        "robot": robot_data
    }

# WebSocket endpoint here
@app.websocket("/web_socker_endpoint")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = f"{websocket.client.host}:{websocket.client.port}"
    print(f"New WebSocket connection from {client}")
    
    # Send initial data
    await websocket.send_json({
        "type": "connected",
        "message": "Connected to robot WebSocket",
        "timestamp": datetime.now().isoformat(),
        "robot": robot_data
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Command from {client}: {data}")
            
            try:
                command = json.loads(data)
                response = {
                    "type": "response",
                    "timestamp": datetime.now().isoformat(),
                    "received": command,
                }
                

                if "command" in command:
                    if command["command"] == "move":
                        if "position" in command:
                            robot_data["position"] = command["position"]
                            response["status"] = "success"
                            response["message"] = "Robot moved to new position"
                        else:
                            response["status"] = "error"
                            response["message"] = "Missing position data"
                    
                    elif command["command"] == "get_data":
                        # Update with random dummy data
                        robot_data["battery"] = max(0, min(100, robot_data["battery"] + random.uniform(-1, 0.5)))
                        robot_data["sensors"]["temperature"] = round(robot_data["sensors"]["temperature"] + random.uniform(-0.2, 0.2), 1)
                        response["status"] = "success"
                        response["message"] = "Robot data retrieved"
                        response["robot"] = robot_data
                    
                    else:
                        response["status"] = "error"
                        response["message"] = f"Unknown command: {command['command']}"
                else:
                    response["status"] = "error"
                    response["message"] = "Missing command field"
                
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON command",
                    "received": data,
                    "timestamp": datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        print(f"WebSocket connection closed: {client}")

if __name__ == "__main__":
    print(f"Starting Robot API server...")
    print(f"Certificate: {CERT_FILE}")
    print(f"Private key: {KEY_FILE}")
    print(f"Visit: https://localhost:8443/")
    print(f"WebSocket: wss://localhost:8443/ws")
    print("(You'll need to accept the security warning since we're using a self-signed certificate)")
    

    uvicorn.run(
        "robot_api:app", 
        host="localhost", 
        port=8443,
        ssl_keyfile=KEY_FILE,
        ssl_certfile=CERT_FILE
    ) 