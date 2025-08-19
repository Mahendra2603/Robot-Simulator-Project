# **Robot Controller – Autonomous Simulation 🤖**

## **Overview**

This project provides an autonomous robot controller with a real-time, web-based simulator. The robot is designed to navigate a pre-defined path, set goals, avoid collisions, and respond to live commands via a WebSocket interface.

## **✨ Features**

* **Autonomous Path Following**: The main controller script automatically computes the path to a goal.  
* **Real-time Web Simulator**: Visualize the robot's movement and interactions in your browser.  
* **Collision Detection**: The simulator tracks and reports collisions.  
* **API-Driven Control**: A Flask API exposes simple endpoints to move, stop, and set goals for the robot.  
* **Live WebSocket Communication**: Commands are sent to the simulator in real-time for instant feedback.

## **⚙️ System Architecture**

The system is composed of several key components that work together:

* **Flask API (server.py)**: Exposes HTTP endpoints for high-level commands like move, stop, and set\_goal.  
* **WebSocket Server (server.py)**: Sits alongside the Flask API to broadcast commands live to all connected simulators.  
* **Browser Simulator (index.html)**: The frontend that visualizes the robot and executes movement commands received via WebSocket.  
* **Main Controller (main\_controller.py)**: The "brain" of the robot. It calculates the path and sends a sequence of commands to the API to reach the goal.  
* **API Client (api\_client.py)**: A convenient wrapper that simplifies making HTTP requests to the Flask API from the controller.

## **📁 Folder Structure**

robot\_controller/  
├── sim-1/                \# Simulator code (browser-based)  
│   ├── index.html        \# Simulator interface  
│   └── server.py         \# Flask \+ WebSocket server  
├── api\_client.py         \# API wrapper for robot commands  
├── vision.py             \# (Optional) Vision processing code  
├── main\_controller.py    \# Main robot path execution script  
└── requirements.txt      \# Python dependencies

## **🚀 Getting Started**

### **Prerequisites**

* Python 3.11+  
* A modern web browser (Chrome, Firefox, or Edge)

### **Installation**

1. Clone the repository or download the source code.  
2. Navigate to the project's root directory.  
3. Install the required Python dependencies using the requirements.txt file:  
   pip install \-r requirements.txt

4. **(Optional)** For advanced calculations or debugging, you may want to install numpy and matplotlib:  
   pip install numpy matplotlib

## **🎮 How to Run**

Follow these steps in order to get the simulation running.

### **Step 1: Start the Server**

First, launch the backend server which handles API requests and WebSocket communication.

\# Navigate into the simulator directory  
cd sim-1

\# Run the server script  
python server.py

You should see a confirmation in your terminal:

✅ WebSocket running on ws://localhost:8765  
✅ Flask API running on http://127.0.0.1:5000

### **Step 2: Open the Simulator**

Open the sim-1/index.html file directly in your web browser. Open the browser's developer console (usually by pressing F12) to confirm the connection. You should see:

✅ Connected to server WebSocket

### **Step 3: Run the Main Controller**

Finally, open a **new terminal window**, navigate to the project's root directory, and run the main controller script.

\# Make sure you are in the root 'robot\_controller' directory  
python main\_controller.py

The robot in the browser simulator will immediately start moving along its pre-defined path. Your terminal will show live updates of the robot's pose, commands being sent, and its distance to the goal.

## **🕹️ API Endpoints**

The Flask server provides the following endpoints to control the robot.

| Endpoint | Method | Description | JSON Payload Example |
| :---- | :---- | :---- | :---- |
| /move | POST | Move robot to an absolute position. | { "x": 150, "z": 200 } |
| /move\_rel | POST | Move robot by a relative turn and distance. | { "turn": 10, "distance": 25 } |
| /goal | POST | Set the visual goal marker's position. | { "x": 400, "z": 400 } |
| /stop | POST | Stop the robot immediately. | (None) |
| /collisions | GET | Get the current number of collisions. | (None) |
| /reset | POST | Reset collision count and robot position. | (None) |

## **🤔 Troubleshooting**

**Error: "No simulators connected"**

* Make sure index.html is open and running in your browser.  
* Confirm the WebSocket connection message appears in the browser console.  
* Ensure server.py was started *before* you opened the simulator page.

**Commands Not Executing**

* Check that the command names (move\_rel, move, goal, stop) in the server.py broadcast function match the names handled in the simulator's JavaScript code.

**WebSocket Errors (RuntimeError: no running event loop)**

* This can happen when mixing asyncio with a threaded server like Flask. Ensure you are using a threaded asyncio implementation in server.py and that the broadcast() function uses the correct event loop, for example:  
  asyncio.run\_coroutine\_threadsafe(ws.send(msg\_json), asyncio.get\_event\_loop())

**Distance to Goal Not Decreasing**

* Double-check that the goal coordinates in main\_controller.py are correct and reachable.  
* You may need to fine-tune the turn angle and step size values in the controller script for more efficient movement.

## **📝 Notes & Recommendations**

* You can predefine complex paths, waypoints, and obstacles in main\_controller.py.  
* The optional vision.py file is a great place to implement computer vision logic for dynamic obstacle detection.  
* The server is capable of broadcasting to multiple simulators at once. Just open index.html in several browser tabs.
