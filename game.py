import pyxel
from positioning import *
from drawing import Camera
from world_data import *
from random import randint
from math import floor

class Player:
    def __init__(self, camera: Camera, move_speed: float, rotate_speed: float):
        self.camera = camera
        self.move_speed = move_speed
        self.rotate_speed = rotate_speed
        self.last_selected: Convex_quad_3D = ""

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

    def find_targeted_quad(self, world: World):
        movement_vector_x = -pyxel.sin(self.camera.yaw) * pyxel.cos(self.camera.pitch)
        movement_vector_z = pyxel.cos(self.camera.yaw) * pyxel.cos(self.camera.pitch)
        movement_vector_y = -pyxel.sin(self.camera.pitch)

        movement_vector = Point3D(movement_vector_x, movement_vector_y, movement_vector_z)

        position = self.camera.position.clone()

        found = False

        while position.distance_to(self.camera.position) < 5:
            amounts_to_move = Point3D(1 - (position.x - 0.5) % 1 if movement_vector_x > 0 else (position.x - 0.5) % 1, 
                                      1 - (position.y - 0.5) % 1 if movement_vector_y > 0 else (position.y - 0.5) % 1, 
                                      1 - (position.z - 0.5) % 1 if movement_vector_z > 0 else (position.z - 0.5) % 1)
        
            options: dict[str, float] = dict()

            if movement_vector_x != 0:
                options["x"] = abs(amounts_to_move.x / movement_vector_x)
            if movement_vector_y != 0:
                options["y"] = abs(amounts_to_move.y / movement_vector_y)
            if movement_vector_z != 0:
                options["z"] = abs(amounts_to_move.z / movement_vector_z)
            
            smallest = min(options.values()) if min(options.values()) > 0.001 else 0.001

            position += movement_vector * smallest

            block_chunk = floor(round(position + movement_vector * 0.001) / CHUNK_SIZE)
            block_position = round(position + movement_vector * 0.001) - block_chunk * CHUNK_SIZE


            if world.chunks[(block_chunk.x, block_chunk.y, block_chunk.z)].get_block(block_position.x, block_position.y, block_position.z) != 0:
                found = True
                break
        
        if found:
            quad_pos: Point3D
            if abs(position.x % 1 - 0.5) < 0.001:
                quad_pos = Point3D(round(position.x - 0.5) + 0.5, round(position.y), round(position.z))
            elif abs(position.y % 1 - 0.5) < 0.001:
                quad_pos = Point3D(round(position.x), round(position.y - 0.5) + 0.5, round(position.z))
            else:
                quad_pos = Point3D(round(position.x), round(position.y), round(position.z - 0.5) + 0.5)

            quad_chunk = floor(round(quad_pos + movement_vector * 0.001) / CHUNK_SIZE)

            if quad_pos in world.chunks[(quad_chunk.x, quad_chunk.y, quad_chunk.z)].quads:
                world.chunks[(quad_chunk.x, quad_chunk.y, quad_chunk.z)].quads[quad_pos].selected = True

                if self.last_selected and world.chunks[(quad_chunk.x, quad_chunk.y, quad_chunk.z)].quads[quad_pos] != self.last_selected:
                    self.last_selected.selected = False
                self.last_selected = world.chunks[(quad_chunk.x, quad_chunk.y, quad_chunk.z)].quads[quad_pos]
    
        elif self.last_selected:
            self.last_selected.selected = False

class GUI:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
    
    def draw_crosshair(self):
        crosshair_radius = round(self.WIDTH / 80)
        crosshair_weight = round(crosshair_radius / 4)

        pyxel.rect(self.WIDTH / 2 - crosshair_weight / 2, self.HEIGHT / 2 - crosshair_radius, crosshair_weight, crosshair_radius * 2, 7)
        pyxel.rect(self.WIDTH / 2 - crosshair_radius, self.HEIGHT / 2 - crosshair_weight / 2, crosshair_radius * 2, crosshair_weight, 7)
    
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
        self.gui = GUI(self.WIDTH, self.HEIGHT)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.f += 1
        self.player.move() 
        self.world.generate_necessary_chunks(self.player.camera.position, self.f)
        self.player.find_targeted_quad(self.world)

    def draw(self):
        self.player.camera.draw_world(self.world, self.f)
        self.gui.draw_crosshair()