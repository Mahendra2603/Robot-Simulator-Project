# 🤖 Robot Control Simulator

The **Robot Control Simulator** provides a simple robot control environment with a **3D visualizer**, a **Flask API server**, and a **client API**.  
It allows you to send commands to a simulated robot, visualize its movements, detect collisions, and reach goals — all in your web browser.

---

## 🚀 Features

- **3D Simulator**  
  Web-based simulator built with **Three.js** to visualize the robot, obstacles, and goals.  

- **API Server**  
  A **Flask server** exposing REST API endpoints for robot control.  

- **WebSocket Communication**  
  Real-time communication between the server and simulator for instant command execution & status updates.  

- **Client Libraries**  
  - `api_client.py` → Python wrapper for the API  
  - `main_controller.py` → High-level controller script to demonstrate goal setting and movement  

- **Vision Module**  
  Basic computer vision (`vision.py`) using **OpenCV** & **PIL** to detect obstacles and goals by color.  

---

## 🏗️ System Architecture

- **server.py** → Flask app running REST API + WebSocket server.  
- **index.html** → Frontend 3D simulator (Three.js).  
- **api_client.py** → Python wrapper for REST API.  
- **main_controller.py** → Example script to command the robot.  
- **vision.py** → Image processing utilities.  
- **requirements.txt** → Required Python dependencies.  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone <repository_url>
cd <repository_name>
2️⃣ Install dependencies
It is recommended to use a virtual environment.

bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Start the server
bash
Copy
Edit
python server.py
You should see logs indicating Flask API and WebSocket are running.

4️⃣ Open the simulator
Open index.html in a modern browser (Chrome, Firefox).
You should see the connection status as CONNECTED.

5️⃣ Run the controller
bash
Copy
Edit
python main_controller.py
The robot will be commanded to move to (30, 30) and animate in the simulator.

📡 API Endpoints
Method	Endpoint	Description	Example JSON Body
POST	/move_rel	Move robot relative distance & turn	{"turn": 90, "distance": 10}
POST	/move	Move robot to absolute position	{"x": 20, "z": 15}
POST	/goal	Set goal marker in simulator	{"x": 30, "z": 30}
POST	/stop	Stop robot movement	{}
📦 Dependencies

All Python dependencies are listed in requirements.txt:

Flask

requests

opencv-python

numpy

Pillow

Install via:

pip install -r requirements.txt

🛠️ Future Improvements

Add multiple robots in the simulation.

Implement advanced path-planning algorithms (A*, Dijkstra).

Extend vision module with deep learning models.

Support for joystick / gamepad control.
