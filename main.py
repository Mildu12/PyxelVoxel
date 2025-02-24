import pyxel
from positioning import *
from drawing import Camera
from world_data import *
from random import randint

position = Point3D(0.0, 0.0, 0.0)
move_speed = 6.0
rotate_speed = 60

WIDTH, HEIGHT = int(160 * 4), int(120 * 4)
FPS = 30
render_distance = 3
fov = 105
f = 0

pyxel.init(WIDTH, HEIGHT, "Minexel", fps=FPS)

def clamp(x, max, min):
    if x > max:
        return max
    if x < min:
        return min
    return x

world = World(randint(0, 100), render_distance)
main_cam = Camera(Point3D(0.0, world.get_terrain_height_at_point(Point3D(0, 0, 0)) + 2, 0.0), fov, WIDTH, HEIGHT)

def update():
    global fov, f
    f += 1
    #Moving the camera forwards, backwards, left, right
    if pyxel.btn(pyxel.KEY_W):
        main_cam.position.x -= move_speed / FPS * pyxel.sin(main_cam.yaw)
        main_cam.position.z += move_speed / FPS * pyxel.cos(main_cam.yaw)
    if pyxel.btn(pyxel.KEY_S):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw)
    if pyxel.btn(pyxel.KEY_A):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw - 90)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw - 90)
    if pyxel.btn(pyxel.KEY_D):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw + 90)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw + 90)


    #Moving the camera up, down
    if pyxel.btn(pyxel.KEY_SPACE):
        main_cam.position.y += move_speed / FPS
    if pyxel.btn(pyxel.KEY_LSHIFT):
        main_cam.position.y -= move_speed / FPS

    #Rotating the camera
    if pyxel.btn(pyxel.KEY_LEFT):
        main_cam.rotate(0.0, +rotate_speed / FPS)
    if pyxel.btn(pyxel.KEY_RIGHT):
        main_cam.rotate(0.0, -rotate_speed / FPS)
    if pyxel.btn(pyxel.KEY_UP):
        main_cam.rotate(-rotate_speed / FPS, 0.0)
    if pyxel.btn(pyxel.KEY_DOWN):
        main_cam.rotate(+rotate_speed / FPS, 0.0)
   
    world.generate_necessary_chunks(main_cam.position, f)

def draw():
    main_cam.draw_world(world, f)

pyxel.run(update, draw)