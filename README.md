# Pygame + C++ 3D Raycaster

A 3D raycaster engine built using Python and Pygame. To optimize performance, the intensive mathematical ray-surface collision calculations are offloaded to a native C++ extension module. Communication between Python and C++ is handled via `pybind11`.

## Features

* **C++ Extension Core:** Raycasting logic and grid coordinate validation run natively in C++ to maintain a stable frame rate.
* **Direct Memory Binding:** Utilizes `pygame.surfarray` to pass Pygame surface pixel data directly to C++ as 3D arrays without copying memory over the language barrier.
* **Mouse Look:** Hardware-bound relative mouse tracking using the horizontal mouse delta (`rel_x`) for seamless 360-degree camera rotation.
* **Dynamic Depth Shading:** Walls are progressively darkened based on the calculated distance to simulate depth fog.
* **AZERTY Movement Vectors:** Configured out-of-the-box for `Z`, `S`, `Q`, `D` inputs, moving the player dynamically relative to the camera orientation.

## Prerequisites

* Python 3.11+
* Pygame
* NumPy
* pybind11
* A C++ compiler supporting at least C++17 (e.g., GCC/MinGW via MSYS2 or MSVC)

## Installation & Compilation

1. Activate your virtual environment and install the required packages:
   ```bash
   pip install pygame numpy pybind11 setuptools
   ```

2. Compile the C++ extension module manually via PowerShell (adjust paths to match your system installation if necessary):
   ```powershell
   g++ -O3 -shared -std=c++17 -fPIC -IC:\Users\daan.eeckloo\AppData\Local\Programs\Python\Python311\Include -IC:\Users\daan.eeckloo\Documents\thuis\cocktail_game\cocktail_venv\Lib\site-packages\pybind11\include -LC:\Users\daan.eeckloo\AppData\Local\Programs\Python\Python311\libs raycasting.cpp -o raycasting.pyd -lpython311 -static -lstdc++ -lgcc -lwinpthread
   ```
   *This generates `raycasting.pyd` directly inside your project directory, making it ready to be imported into your Python scripts.*

## Controls

* **`Z` / `S`** – Move Forward / Backward (relative to camera viewpoint)
* **`Q` / `D`** – Strafe Left / Strafe Right
* **`Mouse`** – 360° Camera Look (The cursor is automatically hidden and captured)
* **`ESC`** – Release mouse control / Exit focus

## Code Snippet Example

In Python, capture the raw memory slice of the surface and send it into the compiled binary:

```python
import pygame
import pygame.surfarray as surfarray
import raycasting

# Access the surface memory directly as a NumPy view
pixel_values = surfarray.pixels3d(rendered_surface)

# Compute ray distances natively
distances = raycasting.cast(
    fov, pixel_width, current_angle, wall_color, 
    current_cord, current_pixel, pixel_values
)
```

In C++, read the multi-dimensional buffer layout without type conversion delays:

```cpp
// Accept the 3D NumPy array from Python
py::array_t<uint8_t> pixel_values;

// Unchecked data views allow raw pointer indexing inside the loop for maximum speed
auto grid = pixel_values.unchecked<3>(); 
uint8_t r = grid(px, py, 0); 
```

## License

This project is licensed under the [MIT License](LICENSE).
