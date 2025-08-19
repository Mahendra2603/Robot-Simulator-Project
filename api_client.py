import requests

class RobotAPI:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip("/")

    def set_goal(self, x, z):
        try:
            resp = requests.post(f"{self.base_url}/goal", json={"x": x, "z": z})
            resp.raise_for_status()  # Raise exception for bad status codes
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to set goal: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error setting goal: {str(e)}"}

    def move_relative(self, turn=0, distance=1.5):
        try:
            resp = requests.post(f"{self.base_url}/move_rel", json={"turn": turn, "distance": distance})
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to move: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error moving: {str(e)}"}

    def move_absolute(self, x, z):
        try:
            resp = requests.post(f"{self.base_url}/move", json={"x": x, "z": z})
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to move absolute: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error moving absolute: {str(e)}"}

    def stop(self):
        try:
            resp = requests.post(f"{self.base_url}/stop")
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to stop: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error stopping: {str(e)}"}

    def get_collisions(self):
        try:
            resp = requests.get(f"{self.base_url}/collisions")
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get collisions: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error getting collisions: {str(e)}"}

    def get_status(self):
        """Get general status of the robot/server"""
        try:
            resp = requests.get(f"{self.base_url}/status")
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get status: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error getting status: {str(e)}"}