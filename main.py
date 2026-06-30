import pygame
import json
import math
import raycasting

rendered_window_width = 603
rendered_window_height = 604

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
rendered_surface = pygame.Surface((rendered_window_width, rendered_window_height))
pygame.display.set_caption("3D maze")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

rows = 30
columns = 30
rendered_walls_left = []
rendered_walls_top = []
wall_color = (0,255,0)
floor_color = (0,0,0)
running = True
current_pixel = (5, 20)
current_cord = (0, 0)
current_angle = 315

#constants:
movement_speed = 5
fov = 45
pixel_width = 12
render_distance = 160
projection_constant = 100000
mouse_sensitivity = 0.15

with open("maze.json", "r") as f:
    raw_unloaded_data = json.load(f)
    rendered_walls_left = raw_unloaded_data["left_walls"]
    rendered_walls_top = raw_unloaded_data["top_walls"]

rendered_surface.fill(floor_color)
for row in range(rows):
    for column in range(columns):
        x,y = column * 20, row * 20
        if rendered_walls_left[row][column]:
            pygame.draw.rect(rendered_surface, wall_color, (x,y,3,20))
        if rendered_walls_top[row][column]:
            pygame.draw.rect(rendered_surface, wall_color, (x,y,20,3))
pygame.draw.rect(rendered_surface, wall_color, (600, 0, 3, 600))
pygame.draw.rect(rendered_surface, wall_color, (0, 600, 600, 3))

pixel_matrix = pygame.surfarray.pixels3d(pygame.transform.scale_by(rendered_surface, 1))

def distance_to_color(distance):
    if distance > render_distance * pixel_width:
        return (0, 0, 0)
    else:
        distance_jump = 255 / (render_distance * pixel_width)
        return (0, math.floor(distance_jump * ((render_distance * pixel_width) - distance)), 0)
    
def get_dist_to_ceil(ray_length):
    wall_height = projection_constant / ray_length
    return round((600 - wall_height) / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    # player movement
    if True: 
        rel_x, rel_y = pygame.mouse.get_rel()
        current_angle += rel_x * mouse_sensitivity

        keys = pygame.key.get_pressed()
        x_plus = 0
        y_plus = 0
        rad = math.radians(current_angle)
        if keys[pygame.K_z]:
            x_plus += math.cos(rad) * movement_speed
            y_plus += math.sin(rad) * movement_speed
        if keys[pygame.K_s]:
            x_plus -= math.cos(rad) * movement_speed
            y_plus -= math.sin(rad) * movement_speed
        if keys[pygame.K_q]:
            x_plus += math.cos(rad - math.pi/2) * movement_speed
            y_plus += math.sin(rad - math.pi/2) * movement_speed
        if keys[pygame.K_d]:
            x_plus += math.cos(rad + math.pi/2) * movement_speed
            y_plus += math.sin(rad + math.pi/2) * movement_speed
        
        if x_plus != 0 or y_plus != 0:
            # calculating new x cord
            if x_plus != 0:
                next_sub_x = current_cord[0] + x_plus
                if 0 <= next_sub_x <= pixel_width:
                    current_cord = (next_sub_x, current_cord[1])
                elif next_sub_x < 0:
                    if rendered_surface.get_at((current_pixel[0] - 1, current_pixel[1])) == floor_color:
                        current_pixel = (current_pixel[0] - 1, current_pixel[1])
                        current_cord = (pixel_width + next_sub_x, current_cord[1])
                    else:
                        current_cord = (0, current_cord[1])
                elif next_sub_x > pixel_width:
                    if rendered_surface.get_at((current_pixel[0] + 1, current_pixel[1])) == floor_color:
                        current_pixel = (current_pixel[0] + 1, current_pixel[1])
                        current_cord = (next_sub_x - pixel_width, current_cord[1])
                    else:
                        current_cord = (pixel_width, current_cord[1])
            #calculating new y cord
            if y_plus != 0:
                next_sub_y = current_cord[1] + y_plus
                if 0 <= next_sub_y <= pixel_width:
                    current_cord = (current_cord[0], next_sub_y)
                elif next_sub_y < 0:
                    if rendered_surface.get_at((current_pixel[0], current_pixel[1] - 1)) == floor_color:
                        current_pixel = (current_pixel[0], current_pixel[1] - 1)
                        current_cord = (current_cord[0], pixel_width + next_sub_y)
                    else:
                        current_cord = (current_cord[0], 0)
                elif next_sub_y > pixel_width:
                    if rendered_surface.get_at((current_pixel[0], current_pixel[1] + 1)) == floor_color:
                        current_pixel = (current_pixel[0], current_pixel[1] + 1)
                        current_cord = (current_cord[0], next_sub_y - pixel_width)
                    else:
                        current_cord = (current_cord[0], pixel_width)

    # C++ function call
    distances = raycasting.cast(fov, pixel_width, current_angle / 1, wall_color, (round(current_cord[0]), round(current_cord[1])), current_pixel, pixel_matrix)

    # displaying
    screen.fill(floor_color)
    if True:
        for i in range(800):
            ray_length = distances[i]
            if ray_length == 0:
                ray_length = 0.1
            color = distance_to_color(ray_length)
            dist_to_ceil = get_dist_to_ceil(ray_length)
            pygame.draw.line(screen, color, (i, dist_to_ceil), (i, 600 - dist_to_ceil))
    pygame.display.update()
    clock.tick(60)