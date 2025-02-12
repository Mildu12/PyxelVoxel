import pyxel
from positioning import *
from drawing import Camera
from world_data import *

position = Point3D(0.0, 0.0, 0.0)
move_speed = 6.0
rotate_speed = 60

WIDTH, HEIGHT = int(160 * 1.5), int(90 * 1.5)
FPS = 60
fov = 90

pyxel.init(WIDTH, HEIGHT, "Minexel", fps=FPS)

def clamp(x, max, min):
    if x > max:
        return max
    if x < min:
        return min
    return x

main_cam = Camera(Point3D(0.0, 1.0, -5.0), fov, WIDTH, HEIGHT)
chunk = Chunk(Point3D(0, 0, 0))

def update():
    global fov
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

    if pyxel.btn(pyxel.KEY_E):
        fov += 1
        main_cam.change_fov(fov)
    if pyxel.btn(pyxel.KEY_Q):
        fov -= 1
        main_cam.change_fov(fov)
   
def draw():
    pyxel.cls(6)
    main_cam.gather_quads_from_chunk(chunk)
    main_cam.filter_quads()
    main_cam.sort_quads()
    main_cam.draw_all_quads()

pyxel.run(update, draw)