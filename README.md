
Robot Control Simulator
This project provides a simple robot control simulation environment, including a 3D visualizer, a control server, and a client API. The system allows you to send commands to a simulated robot and visualize its movement, collision detection, and goal-reaching in a web browser.

Features
3D Simulator: A web-based 3D simulation built with Three.js that visualizes the robot, obstacles, and a target goal.

API Server: A Flask server that exposes REST API endpoints for controlling the robot.

WebSocket Communication: Real-time communication between the Flask server and the web simulator using WebSockets for instant command execution and status updates.

Client Libraries: Python classes for interacting with the API server (api_client.py) and for a high-level robot controller (main_controller.py).

Vision Module: A basic computer vision script (vision.py) to process simulated camera images and detect obstacles or goals based on color.

System Architecture
server.py: A Flask application that runs a REST API and a WebSocket server.

REST API: Receives commands (e.g., move_rel, move) from clients.

WebSocket: Broadcasts these commands in real-time to connected simulators (index.html). It also receives status updates from the simulator, such as collision notifications.

index.html: The front-end simulator.

Connects to the server.py WebSocket.

Renders the 3D scene (robot, floor, obstacles, goal) using Three.js.

Listens for commands from the WebSocket and animates the robot's movement accordingly.

Detects collisions and goal-reaching, and sends notifications back to the server.

api_client.py: A Python class that provides a simple wrapper for making HTTP requests to the server.py REST API. This is the primary way to programmatically control the robot.

main_controller.py: An example script that uses the RobotAPI class to set a goal and command the robot to move to that absolute position. This demonstrates a basic control flow.

vision.py: Contains helper functions using OpenCV for basic image processing. It's designed to analyze a robot's "camera feed" (though not fully implemented in the main flow) to identify objects based on color, such as green obstacles and the cyan goal.


requirements.txt: Lists all the necessary Python dependencies for the project, including requests, opencv-python, numpy, and Pillow. 

Getting Started
Follow these steps to set up and run the simulation.

Clone the repository:

Bash

git clone <repository_url>
cd <repository_name>
Install dependencies:
Make sure you have Python installed. It is recommended to use a virtual environment.

Bash

pip install -r requirements.txt
Start the server:
Open a terminal and run the Flask server. This will also start the WebSocket server in a background thread.

Bash

python server.py
You should see output indicating that the Flask API and WebSocket are running.

Open the simulator:
Open the index.html file in a modern web browser (e.g., Chrome, Firefox). The simulator should connect automatically to the server. The connection status in the top-right corner of the page should change from "DISCONNECTED" to "CONNECTED".

Run a control script:
In a new terminal, run the example controller script to command the robot.

Bash

python main_controller.py
This script will command the robot to move to the goal at coordinates (30, 30). You will see the robot animate this movement in the browser simulator.

API Endpoints
The server.py exposes the following REST API endpoints:

POST /move_rel: Moves the robot a relative distance and turns.

JSON Body: {"turn": <degrees>, "distance": <units>}

POST /move: Commands the robot to move to an absolute position.

JSON Body: {"x": <x_coord>, "z": <z_coord>}

POST /goal: Sets the goal marker in the simulator.

JSON Body: {"x": <x_coord>, "z": <z_coord>}

POST /stop: Stops any ongoing robot movement.

GET /status: Returns the general status of the server/robot.

GET /collisions: Returns information about collisions (not fully implemented in the current flow).
