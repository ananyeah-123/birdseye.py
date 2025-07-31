# birdseye.py
A custom control interface for the CARLA simulator that lets you spawn, drive, and switch between multiple vehicles in real time—complete with camera presets, HUD, minimap, and manual gear controls inspired by CARLA's native manual_control.py
Here’s a professional and concise `README.md` description you can use for your GitHub repository:

---

## 🏎️ CARLA Multi-Vehicle Manual Control Interface

This repository provides an extended manual control interface for the [CARLA Simulator](https://carla.org/), enabling real-time control and visualization of multiple vehicles. Inspired by CARLA's `manual_control.py`, this version supports:

### 🔧 Features

* 🚘 **Spawn and control multiple vehicles** on the map
* 🔁 **Switch control between cars** using a single key (`C`)
* 🧭 **Three camera perspectives**:

  * Bird's-eye (mouse-pan and zoomable)
  * Chase (3rd-person follow)
  * Driver (1st-person dashboard)
* 🧠 **Manual driving controls** identical to `manual_control.py`:

  * Reverse gear (`Q`)
  * Manual gear shifting (`M`, `,`, `.`)
  * Handbrake (`Space`)
  * Autopilot toggle (`P`)
  * Constant velocity mode (`Ctrl + W`)
* 🧩 **Camera sensor switching** (`RGB`, `Depth`, `Semantic Segmentation`)
* 🗺️ **Mini-map overlay** for visualizing all vehicles
* 🧾 **On-screen HUD**: speed, gear, active car ID, camera mode
* 📜 **In-app help menu** (`H`) and HUD toggle (`F1`)

### 🚀 Getting Started

1. Launch CARLA:

   ```bash
   ./CarlaUE4.sh    # or CarlaUE5.sh depending on your version
   ```

2. Copy paste birdseye.py in Carla-> PythonAPI-> examples and run the script:

   ```bash
   cd PythonAPI/examples
   python3 birdseye.py
   ```

### 💡 Requirements

* Python 3.8–3.10
* [CARLA Simulator 0.9.13+](https://github.com/carla-simulator/carla/releases)
* `pygame`:

  ```bash
  pip install pygame
  ```

### 🎮 Controls Summary

| Action              | Key           |
| ------------------- | ------------- |
| Throttle / Brake    | W / S         |
| Steer               | A / D         |
| Reverse             | Q             |
| Handbrake           | Space         |
| Manual Gear Mode    | M             |
| Gear Up / Down      | . / ,         |
| Autopilot Toggle    | P             |
| Constant Velocity   | Ctrl + W      |
| Switch Vehicle      | C             |
| Camera View Presets | V             |
| Sensor Type Switch  | \` (Backtick) |
| Help / HUD Toggle   | H / F1        |
| Exit                | ESC           |

---

Let me know if you'd like badges (e.g., Python version, license, stars) or screenshots added!
