#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <cmath>
#include <vector>

const double pi = 3.14159265359;

namespace py = pybind11;

double deg_to_rad(double degrees) {
    return degrees * (pi / 180.0);
}

py::array_t<float> cast_rays(uint8_t fov, int pixel_size, float current_angle, std::tuple<uint8_t, uint8_t, uint8_t> wall_color, std::tuple<int, int> current_cord, std::tuple<int, int> current_pixel, py::array_t<uint8_t> pixel_values) {
    auto grid = pixel_values.unchecked<3>();
    float angle_base = current_angle - (fov / 2);
    double ray_jump = fov / 800.0;

    std::vector<float> distances;
    distances.reserve(800);

    for (int i = 0; i < 800; i++ ) {
        double angle = angle_base + i * ray_jump;
        float pixel_x = std::get<0>(current_pixel);
        float pixel_y = std::get<1>(current_pixel);
        auto [wall_r, wall_g, wall_b] = wall_color;

        while (grid(std::round(pixel_x), std::round(pixel_y), 0) != wall_r || grid(std::round(pixel_x), std::round(pixel_y), 1) != wall_g || grid(std::round(pixel_x), std::round(pixel_y), 2) != wall_b) {
            pixel_x += std::cos(deg_to_rad(angle));
            pixel_y += std::sin(deg_to_rad(angle));
        }

        float x_dist;
        float y_dist;
        
        if (pixel_x > std::get<0>(current_pixel)) {
            x_dist = (pixel_size - std::get<0>(current_cord)) + pixel_size * (pixel_x - std::get<0>(current_pixel));
        }
        else {
            x_dist = std::get<0>(current_cord) + pixel_size * (std::get<0>(current_pixel) - pixel_x);
        }

        if (pixel_y > std::get<1>(current_pixel)) {
            y_dist = (pixel_size - std::get<1>(current_cord)) + pixel_size * (pixel_y - std::get<1>(current_pixel));
        }
        else {
            y_dist = std::get<1>(current_cord) + pixel_size * (std::get<1>(current_pixel) - pixel_y);
        }

        float final_dist = std::sqrt(x_dist * x_dist + y_dist * y_dist);
        distances.push_back(final_dist);
    }

    float* raw_ptr = distances.data();

    auto capsule = py::capsule(new std::vector<float>(std::move(distances)), [](void *p) {
        delete reinterpret_cast<std::vector<float> *>(p);
    });

    return py::array_t<float>(
        {static_cast<ssize_t>(800)},
        {sizeof(float)},
        raw_ptr,
        capsule
    );

}

PYBIND11_MODULE(raycasting, m) {
    m.def("cast", &cast_rays, "A function that finds the the distance to the closest wall in all directions.");
}