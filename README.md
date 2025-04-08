# Robot Control Proof of Concept

This is a minimal proof of concept for testing secure communications between a web client and a robot API server using self-signed certificates over HTTPS and WebSockets.

## Architecture

The POC has two main components:

1. **Static Dashboard**: Serves the client HTML/JS.

2. **Robot API Server**: A FastAPI server that:
   - Provides HTTPS endpoints for robot status
   - Provides WebSocket endpoint for real-time communication
   - Uses self-signed certificates for secure communication
   - Runs on port 8443

The key challenge this POC addresses is the connection from the client's browser to the robot API server using self-signed certificates.

## Prerequisites

- Python 3.7+
- FastAPI and Uvicorn (for the robot server)
- openSSL (for generating the self-signed certificates) {though the self-signed certificates are already provided in the `certs` directory}

## Setup

1. Make sure you have the required packages installed in your virtual environment:
   ```
   pip install fastapi uvicorn
   ```

2. The self-signed certificates are already provided in the `certs` directory.

## Running the POC

### 1. Start the Robot API Server

```
cd robot_server
python robot_api.py
```

This will start the robot API server on port 8443.

### 2. Access the Client

Open your file explorer and navigate to: ../static_server/standalone_client.html

### 3. Installing the self-signed certificate

Get the certificate from the `certs` directory and install it in your browser.
Steps to install the certificate:

1. double click on the certificate file with the name `server.crt`
2. click on the `Install Certificate` button
3. click on the `Place all certificates in the following store` button
4. select `Trusted Root Certification Authorities`
5. click `Install`


## Testing the Connection

1. In the client interface, you'll see connection controls with the default settings:
   - Robot URL: localhost
   - Robot Port: 8443

2. Click "Connect" to establish a WebSocket connection to the robot server.
   - You may see another security warning for the robot server's self-signed certificate
   - Accept this warning to proceed

3. Once connected, you can:
   - Click "Get Status (HTTPS)" to make an HTTPS request to the robot API
   - Click "Get Robot Data" to request data via the WebSocket connection
   - Use the "Move" controls to send movement commands to the robot

4. The "Robot Data" panel will show the current robot state.

5. The "Command Log" panel will show all interaction history.