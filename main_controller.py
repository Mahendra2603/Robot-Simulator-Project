import time
import math
import requests

# ------------------------------
# Robot API Wrapper
# ------------------------------
class RobotAPI:
    def __init__(self, server_url="http://127.0.0.1:5000"):
        self.server_url = server_url
        self.movement_delay = 2.0  # Increased delay for actual movement

    def move_rel(self, turn=0, distance=1.5):
        try:
            resp = requests.post(f"{self.server_url}/move_rel", json={"turn": turn, "distance": distance})
            data = resp.json()
            if "error" in data:
                print(f"⚠ Error: {data['error']}")
                return False
            print(f"✅ Movement command accepted: turn={turn}°, distance={distance}")
            time.sleep(self.movement_delay)  # Wait for actual movement to complete
            return True
        except Exception as e:
            print(f"⚠ Exception in move_rel: {e}")
            return False

    def move(self, x, z):
        try:
            resp = requests.post(f"{self.server_url}/move", json={"x": x, "z": z})
            data = resp.json()
            if "error" in data:
                print(f"⚠ Error: {data['error']}")
                return False
            print(f"✅ Absolute move command accepted: x={x}, z={z}")
            time.sleep(self.movement_delay)
            return True
        except Exception as e:
            print(f"⚠ Exception in move: {e}")
            return False

    def set_goal(self, x, z):
        try:
            resp = requests.post(f"{self.server_url}/goal", json={"x": x, "z": z})
            data = resp.json()
            if "error" in data:
                print(f"⚠ Error: {data['error']}")
                return False
            print(f"✅ Goal set at: x={x}, z={z}")
            return True
        except Exception as e:
            print(f"⚠ Exception in set_goal: {e}")
            return False

    def stop(self):
        try:
            resp = requests.post(f"{self.server_url}/stop")
            data = resp.json()
            if "error" in data:
                print(f"⚠ Error: {data['error']}")
                return False
            print("✅ Stop command sent")
            return True
        except Exception as e:
            print(f"⚠ Exception in stop: {e}")
            return False

# ------------------------------
# Main Controller Logic
# ------------------------------
if __name__ == "__main__":
    robot = RobotAPI()
    
    # --- Define Goal ---
    goal_x, goal_z = 30, 30

    print(f"🎯 Setting goal marker in simulator at ({goal_x}, {goal_z})...")
    if not robot.set_goal(goal_x, goal_z):
        print("❌ Failed to set goal. Exiting.")
        exit(1)

    print(f"🚀 Sending absolute move command to ({goal_x}, {goal_z})...")
    # The simulator will handle moving the robot from its current position to the goal.
    if not robot.move(goal_x, goal_z):
        print("❌ Movement command failed. Exiting.")
        exit(1)

    # The script has issued the command. The simulator will now animate the robot's movement.
    print("\n✅ Command sent successfully. The robot is now moving towards the goal in the simulator.")
    print("This script has completed its task.")