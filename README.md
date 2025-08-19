Robot Controller – Autonomous Simulation
Overview

This project provides an autonomous robot controller with a web-based simulator. The robot can move along a pre-defined path, set goals, avoid collisions, and interact in real-time via WebSocket. The system uses:

Flask API: Exposes endpoints for commands like move, move relative, stop, and goal setting.

WebSocket Server: Communicates live commands to the simulator.

Browser-based Simulator (index.html): Visualizes the robot and executes movement commands.

Main Controller (main_controller.py): Computes the robot path and sends commands via the API.

API Client (api_client.py): Wrapper for sending requests to the Flask API.

Folder Structure
robot_controller/
├── sim-1/                # Simulator code (browser-based)
│   ├── index.html        # Simulator interface
│   └── server.py         # Flask + WebSocket server
├── api_client.py         # API wrapper for robot commands
├── vision.py             # (Optional) Vision processing code
├── main_controller.py    # Main robot path execution script
└── requirements.txt      # Python dependencies

Dependencies

Make sure Python 3.11+ is installed. Install dependencies:

pip install -r requirements.txt


requirements.txt

Flask>=2.3.2
websockets>=11.0.3
requests>=2.32.0


Optional:

numpy (used in main_controller for calculations)

matplotlib (if you want plotting/debugging)

Browser: Chrome/Firefox to open index.html simulator

Running the Project

Start the Flask + WebSocket server

cd sim-1
python server.py


WebSocket runs on: ws://localhost:8765

Flask API runs on: http://127.0.0.1:5000

Confirm in console:

✅ WebSocket running on ws://localhost:8765
✅ Flask API running on http://127.0.0.1:5000


Open the simulator

Open sim-1/index.html in your browser.

In the browser console, confirm:

✅ Connected to server WebSocket


Run the main controller

python main_controller.py


The robot will follow a pre-defined path towards the goal.

Live updates will be visible in the browser simulator.

The console will show robot pose, commands, and distance to goal.

Available API Endpoints
Endpoint	Method	Description
/move	POST	Move robot to absolute position { "x": float, "z": float }
/move_rel	POST	Move robot relative { "turn": float, "distance": float }
/goal	POST	Set goal position { "x": float, "z": float }
/stop	POST	Stop robot immediately
/collisions	GET	Get number of collisions detected
/reset	POST	Reset collision count and broadcast reset
Main Controller

Computes the robot path automatically.

Sends turn + forward commands to the robot.

Ensures the robot moves towards the goal while avoiding collisions.

Can be customized in main_controller.py for different goals or paths.

Simulator Behavior

Uses WebSocket to receive commands from Flask API.

Commands include:

move_rel → relative motion

move → absolute coordinates

goal → target goal

stop → stop robot

Robot movement and collisions are visualized in real-time.

Troubleshooting

Error: No simulators connected

Make sure index.html is open in the browser.

Confirm WebSocket connection: ws://localhost:8765.

Ensure server.py is running before opening the simulator.

Commands not executing

Ensure command names in server.py match simulator JS:

"move_rel", "move", "goal", "stop".

WebSocket Errors

If RuntimeError: no running event loop occurs:

Use the threaded asyncio event loop implementation in server.py.

Make sure broadcast() uses the correct loop:

asyncio.run_coroutine_threadsafe(ws.send(msg_json), asyncio.get_event_loop())


Distance to goal not decreasing

Confirm main_controller.py uses correct goal coordinates.

Turn angle and step size may need tuning to move efficiently.

Notes / Recommendations

You can predefine paths and obstacles in main_controller.py.

Vision processing can be implemented in vision.py for obstacle detection.

Multiple simulators can connect simultaneously to server.py.

The simulator is browser-based: works best in Chrome or Edge.
