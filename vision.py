# robot_controller/vision.py
import base64
import io
from typing import Dict, Tuple, Optional

import cv2
import numpy as np
from PIL import Image

def dataurl_to_cv2_img(dataurl: str) -> np.ndarray:
    """
    Convert data:image/png;base64,... to an OpenCV BGR image (numpy array).
    """
    if "," in dataurl:
        _, b64 = dataurl.split(",", 1)
    else:
        b64 = dataurl
    raw = base64.b64decode(b64)
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    arr = np.array(im)[:, :, ::-1].copy()  # RGB -> BGR
    return arr

def detect_obstacles_and_goal(img) -> Tuple[Dict, Dict]:
    """
    Detect green obstacles and cyan-ish goal flag in the image.

    Returns:
      obstacle_info: {
         'any': bool,
         'area': int (max contour area),
         'cx': float (pixels) or None,
         'cy': float (pixels) or None,
         'ratio_from_center': float in [-1..1] (negative => left, positive => right)
      }
      goal_info: {
         'seen': bool,
         'cx': float, 'cy': float
      }

    Heuristics are intentionally conservative and easy to tune.
    """
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # --- obstacles: green mask (these are green boxes in index.html) ---
    lower_g = np.array([35, 70, 60])   # hue around green
    upper_g = np.array([90, 255, 255])
    mask_g = cv2.inRange(hsv, lower_g, upper_g)
    kernel = np.ones((5, 5), np.uint8)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_OPEN, kernel)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_area = 0
    best_cx = None
    best_cy = None
    for c in contours:
        area = int(cv2.contourArea(c))
        if area < 50:
            continue
        M = cv2.moments(c)
        if M.get("m00", 0) != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            x, y, ww, hh = cv2.boundingRect(c)
            cx = x + ww // 2
            cy = y + hh // 2
        if area > best_area:
            best_area = area
            best_cx = cx
            best_cy = cy

    obstacle_info = {
        "any": best_area > 0,
        "area": best_area,
        "cx": best_cx,
        "cy": best_cy,
        "ratio_from_center": None
    }
    if best_cx is not None:
        obstacle_info["ratio_from_center"] = (best_cx - (w / 2)) / (w / 2)

    # --- goal: cyan/teal mask (flag color ~ 0x00ccff) ---
    lower_c = np.array([80 - 10, 60, 60])
    upper_c = np.array([100 + 10, 255, 255])
    mask_c = cv2.inRange(hsv, lower_c, upper_c)
    mask_c = cv2.morphologyEx(mask_c, cv2.MORPH_OPEN, kernel)
    contours_c, _ = cv2.findContours(mask_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    goal_seen = False
    gx = gy = None
    best_c_area = 0
    for c in contours_c:
        a = int(cv2.contourArea(c))
        if a < 20:
            continue
        M = cv2.moments(c)
        if M.get("m00", 0) != 0:
            gx = int(M["m10"] / M["m00"])
            gy = int(M["m01"] / M["m00"])
        if a > best_c_area:
            best_c_area = a
            goal_seen = True

    goal_info = {"seen": goal_seen, "cx": gx, "cy": gy}

    return obstacle_info, goal_info
