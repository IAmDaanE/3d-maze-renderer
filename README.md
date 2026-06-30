# 🚀 Hybrid Pygame + C++ 3D Raycaster Engine

A high-performance, retro-style 3D Raycaster engine modeled after classic 90s shooters like *Wolfenstein 3D*. This engine solves the typical Python performance bottleneck by offloading complex mathematical ray-surface collisions to a custom native **C++ extension module**, leveraging **pybind11** for seamless, zero-copy data exchange.

---

## ✨ Features

* **Blazing Fast C++ Core:** Raycasting math, vector calculations, and map/surface inspections run at native C++ speeds.
* **Zero-Copy Memory Interop:** Uses `pygame.surfarray` and `pybind11` to expose raw 3D Pygame surface pixel arrays directly to C++ without heavy copying over the language barrier.
* **Smooth Mouse Look:** Implements hardware-bound relative mouse tracking for effortless 360° camera rotation.
* **Adaptive Depth Fog:** Visually darkens wall slices dynamically based on the calculated distance from the player to create atmospheric depth.
* **AZERTY Input Support:** Configured out-of-the-box for seamless vector movement (`Z`, `S`, `Q`, `D`) relative to the camera's orientation.

---

## 🛠️ Architecture & Tech Stack

The architecture uses **Inversion of Control (IoC)** to optimize the game loop:
1. **Python / Pygame:** Handles windows, context creation, user input, texture surfaces, and final frame blitting.
2. **Pybind11 Bridge:** Directly passes continuous chunks of memory representing surface pixel data down to native code.
3. **C++ Module:** Receives raw pixel maps, computes vector distances via fast Pythagoras math, manages safety boundaries to prevent crashes, and feeds back a specialized, lightweight array of exact ray distances.

---

## 🚀 Getting Started

### 📋 Prerequisites

You will need a Python virtual environment and a C++ compiler supporting at least **C++17** or **C++20** (like MinGW/GCC through MSYS2 on Windows, or Clang on macOS).

```bash
# Clone the repository
git clone https://github.com
cd YOUR_REPO_NAME

# Activate your virtual environment (e.g., cocktail_venv)
# install dependencies
pip install pygame numpy pybind11 setuptools
```

### 🔨 Compiling the C++ Extension

Because Windows system paths can be tricky with GCC, the repository uses a custom automated `setup.py` file to handle library paths, headers, and optimization flags.

To compile the C++ extension module directly into your project workspace, run:

```bash
python setup.py build_ext --inplace
```

*This will generate a native binary (`raycasting.pyd` on Windows or `raycasting.so` on Linux/Mac) that Python can import directly.*

---

## 🎮 How to Play

Run the main game script using your environment's Python interpreter:

```bash
python main.py
```

* **`Z` / `S`** – Move Forward / Backward (relative to viewpoint)
* **`Q` / `D`** – Strafe Left / Right
* **`Mouse`** – 360° Look (Mouse is automatically locked to the center)
* **`ESC`** – Release mouse control / Exit game window

---

## ⚙️ How It Works (Code Insight)

### Python Side (`main.py`)
```python
import pygame
import pygame.surfarray as surfarray
import raycasting  # Your compiled C++ binary!

# Get raw 3D pixel arrays instantly without copying
pixel_values = surfarray.pixels3d(rendered_surface)

# Execute native ray collisions 
distances = raycasting.cast(
    fov, pixel_width, current_angle, wall_color, 
    current_cord, current_pixel, pixel_values
)
```

### C++ Side (`raycasting.cpp`)
```cpp
// Receives the raw NumPy array memory chunk instantly
py::array_t<uint8_t> pixel_values;

// Unchecked data views allow raw pointer indexing inside the loop for maximum speed
auto grid = pixel_values.unchecked<3>(); 
uint8_t r = grid(px, py, 0); 
```

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
