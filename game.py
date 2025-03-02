import pyxel
from positioning import *
from drawing import Camera
from world_data import *
from random import randint

class Player:
    def __init__(self, camera: Camera, move_speed: float, rotate_speed: float):
        self.camera = camera
        self.move_speed = move_speed
        self.rotate_speed = rotate_speed

    def move(self):
        #Moving the camera forwards, backwards, left, right
        if pyxel.btn(pyxel.KEY_W):
            self.camera.position.x -= self.move_speed / 30 * pyxel.sin(self.camera.yaw)
            self.camera.position.z += self.move_speed / 30 * pyxel.cos(self.camera.yaw)
        if pyxel.btn(pyxel.KEY_S):
            self.camera.position.x += self.move_speed / 30 * pyxel.sin(self.camera.yaw)
            self.camera.position.z -= self.move_speed / 30 * pyxel.cos(self.camera.yaw)
        if pyxel.btn(pyxel.KEY_A):
            self.camera.position.x += self.move_speed / 30 * pyxel.sin(self.camera.yaw - 90)
            self.camera.position.z -= self.move_speed / 30 * pyxel.cos(self.camera.yaw - 90)
        if pyxel.btn(pyxel.KEY_D):
            self.camera.position.x += self.move_speed / 30 * pyxel.sin(self.camera.yaw + 90)
            self.camera.position.z -= self.move_speed / 30 * pyxel.cos(self.camera.yaw + 90)


        #Moving the camera up, down
        if pyxel.btn(pyxel.KEY_SPACE):
            self.camera.position.y += self.move_speed / 30
        if pyxel.btn(pyxel.KEY_LSHIFT):
            self.camera.position.y -= self.move_speed / 30

        #Rotating the camera
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.rotate(0.0, +self.rotate_speed / 30)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.rotate(0.0, -self.rotate_speed / 30)
        if pyxel.btn(pyxel.KEY_UP):
            self.camera.rotate(-self.rotate_speed / 30, 0.0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.rotate(+self.rotate_speed / 30, 0.0)


class Game:
    def __init__(self, seed: int = randint(0, 1000), width = 640, height = 480):
        self.WIDTH, self.HEIGHT = width, height
        self.FPS = 30
        self.render_distance = 4
        self.fov = 105
        self.f = 0

        pyxel.init(self.WIDTH, self.HEIGHT, "Minexel", fps=self.FPS)

        self.world = World(seed, self.render_distance)
        camera = Camera(Point3D(0.0, self.world.get_terrain_height_at_point(Point3D(0, 0, 0)) + 2, 0.0), self.fov, self.WIDTH, self.HEIGHT, self.render_distance)
        self.player = Player(camera, 6.0, 60)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.f += 1
        self.player.move()
        self.world.generate_necessary_chunks(self.player.camera.position, self.f)

    def draw(self):
        self.player.camera.draw_world(self.world, self.f)