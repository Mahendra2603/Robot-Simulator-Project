import asyncio
import json
import threading
import websockets
from flask import Flask, request, jsonify

# ------------------------------
# Globals
# ------------------------------
clients = set()
app = Flask(__name__)
ws_loop = None  # Global reference to the WebSocket event loop

# ------------------------------
# WebSocket Handler
# ------------------------------
async def ws_handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[WS] {message}")
    finally:
        clients.remove(websocket)

async def ws_main():
    global ws_loop
    ws_loop = asyncio.get_event_loop()
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        print("✅ WebSocket running on ws://localhost:8765")
        await asyncio.Future()  # run forever

def start_ws():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ws_main())

# ------------------------------
# Helper Functions
# ------------------------------
def broadcast(msg):
    """Send message to all connected WebSocket clients"""
    if not clients:
        return False
    
    msg_json = json.dumps(msg)
    print(f"[API → WS] {msg_json}")
    
    # Use the WebSocket event loop for thread-safe operations
    for ws in list(clients):
        try:
            asyncio.run_coroutine_threadsafe(ws.send(msg_json), ws_loop)
        except Exception as e:
            print(f"[ERR] {e}")
    
    return True

# ------------------------------
# API Endpoints
# ------------------------------
@app.route("/move_rel", methods=["POST"])
def move_rel():
    data = request.get_json()
    msg = {"command": "move_rel", "turn": data.get("turn", 0), "distance": data.get("distance", 1.5)}
    if not broadcast(msg):
        return jsonify({'error': 'No simulators connected'}), 400
    return jsonify({'status': 'move relative command sent', 'command': msg})

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    x = data.get("x", 0)
    z = data.get("z", 0)
    msg = {"command": "move", "x": x, "z": z}
    if not broadcast(msg):
        return jsonify({'error': 'No simulators connected'}), 400
    return jsonify({"status": "ok", "command": msg})

@app.route("/goal", methods=["POST"])
def set_goal():
    data = request.json
    x = data.get("x")
    z = data.get("z")
    msg = {"command": "goal", "x": x, "z": z}
    if not broadcast(msg):
        return jsonify({'error': 'No simulators connected'}), 400
    return jsonify({"status": "ok", "command": msg})

@app.route("/stop", methods=["POST"])
def stop():
    msg = {"command": "stop"}
    if not broadcast(msg):
        return jsonify({'error': 'No simulators connected'}), 400
    return jsonify({"status": "ok", "command": msg})

# ------------------------------
# Main Entrypoint
# ------------------------------
if __name__ == "__main__":
    # Start WebSocket in background thread
    threading.Thread(target=start_ws, daemon=True).start()

    # Run Flask API
    print("✅ Flask API running on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)