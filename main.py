import pyxel
from positioning import *
from drawing import Camera, Block

position = Vector3(0.0, 0.0, 0.0)
move_speed = 6.0
rotate_speed = 120

WIDTH, HEIGHT = int(160 * 1.5), int(120 * 1.5)
FPS = 60
FOV = 90.0

pyxel.init(WIDTH, HEIGHT, "Minexel", fps=FPS)

def clamp(x, max, min):
    if x > max:
        return max
    if x < min:
        return min
    return x

main_cam = Camera(Vector3(0.0, 1.0, 0.0), FOV, WIDTH, HEIGHT)
blocks = [Block(Vector3(j, k, i), 3, 4, 4) for i in range(-5, 0) for j in range(-5, 0) for k in range(-5, 0)]

def len_to_cam(block: Block):
    return block.position.distance_to(main_cam.position)

def update():
    if pyxel.btn(pyxel.KEY_W):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw)
    if pyxel.btn(pyxel.KEY_S):
        main_cam.position.x -= move_speed / FPS * pyxel.sin(main_cam.yaw)
        main_cam.position.z += move_speed / FPS * pyxel.cos(main_cam.yaw)

    if pyxel.btn(pyxel.KEY_A):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw - 90)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw - 90)
    if pyxel.btn(pyxel.KEY_D):
        main_cam.position.x += move_speed / FPS * pyxel.sin(main_cam.yaw + 90)
        main_cam.position.z -= move_speed / FPS * pyxel.cos(main_cam.yaw + 90)

    if pyxel.btn(pyxel.KEY_SPACE):
        main_cam.position.y += move_speed / FPS
    if pyxel.btn(pyxel.KEY_LSHIFT):
        main_cam.position.y -= move_speed / FPS

    if pyxel.btn(pyxel.KEY_LEFT):
        main_cam.rotate(0.0, -rotate_speed / FPS)
    if pyxel.btn(pyxel.KEY_RIGHT):
        main_cam.rotate(0.0, +rotate_speed / FPS)
    if pyxel.btn(pyxel.KEY_UP):
        main_cam.rotate(rotate_speed / FPS, 0.0)
    if pyxel.btn(pyxel.KEY_DOWN):
        main_cam.rotate(-rotate_speed / FPS, 0.0)
    
def draw():
    pyxel.cls(6)
    blocks.sort(key=len_to_cam, reverse=True)
    for block in blocks:
        main_cam.draw_block(block)

pyxel.run(update, draw)