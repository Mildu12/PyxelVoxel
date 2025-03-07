from src.positioning import *
from src.blocks import *
from random import randint
import noise
        
CHUNK_SIZE = 8

class Point_to_project:
    def __init__(self, position_3D: Point3D, current_frame: int):
        self.position_3D: Point3D = position_3D
        self.current_frame: int = current_frame
        self.projected_position: Point2D = Point2D(0, 0)

class Convex_quad_3D:
    def __init__(self, p1: Point_to_project, p2: Point_to_project, p3: Point_to_project, p4: Point_to_project, col: int):
        self.points: list[Point_to_project] = [p1, p2, p3, p4]
        self.col: int = col
        self.selected = False

class Chunk:
    """Container for a 8x8x8 group of blocks"""
    def __init__(self, chunk_position: Point3D):
        self.position = chunk_position
        self.blocks: list[list[list[int]]] = [[[0 for z in range(CHUNK_SIZE)] for y in range(CHUNK_SIZE)] for x in range(CHUNK_SIZE)]
        self.quads: dict[Point3D, Convex_quad_3D] = []

    def generate_quads(self, world: "World", current_frame: int):
        quads: dict[Point3D, Convex_quad_3D] = dict()
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    if self.get_block(x, y, z) != 0:
                        if (x == 0 and ((self.position.x - 1, self.position.y, self.position.z) in world.chunks and world.chunks[(self.position.x - 1, self.position.y, self.position.z)].get_block(CHUNK_SIZE - 1, y, z) == 0 or world.generate_block(Point3D((self.position.x - 1) * CHUNK_SIZE + CHUNK_SIZE - 1, self.position.y * CHUNK_SIZE + y, self.position.z * CHUNK_SIZE + z)) == 0)) or (x != 0 and self.get_block(x - 1, y, z) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x - 0.5, CHUNK_SIZE * self.position.y + y, CHUNK_SIZE * self.position.z + z)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y + 0.5, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y - 0.5, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y - 0.5, quad_pos.z - 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y + 0.5, quad_pos.z - 0.5), current_frame),
                                                        block_types[self.get_block(x, y, z)].side_col
                                                        )
                        

                        if (x == CHUNK_SIZE - 1 and ((self.position.x + 1, self.position.y, self.position.z) in world.chunks and world.chunks[(self.position.x + 1, self.position.y, self.position.z)].get_block(0, y, z) == 0 or world.generate_block(Point3D((self.position.x + 1) * CHUNK_SIZE, self.position.y * CHUNK_SIZE + y, self.position.z * CHUNK_SIZE + z)) == 0)) or (x != CHUNK_SIZE - 1 and self.get_block(x + 1, y, z) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x + 0.5, CHUNK_SIZE * self.position.y + y, CHUNK_SIZE * self.position.z + z)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y + 0.5, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y - 0.5, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y - 0.5, quad_pos.z - 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x, quad_pos.y + 0.5, quad_pos.z - 0.5), current_frame),
                                                        block_types[self.get_block(x, y, z)].side_col
                                                        )

                        if (y == 0 and ((self.position.x, self.position.y - 1, self.position.z) in world.chunks and world.chunks[(self.position.x, self.position.y - 1, self.position.z)].get_block(x, CHUNK_SIZE - 1, z) == 0 or world.generate_block(Point3D(self.position.x * CHUNK_SIZE + x, (self.position.y - 1) * CHUNK_SIZE + CHUNK_SIZE - 1, self.position.z * CHUNK_SIZE + z)) == 0)) or (y != 0 and self.get_block(x, y - 1, z) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x, CHUNK_SIZE * self.position.y + y - 0.5, CHUNK_SIZE * self.position.z + z)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y, quad_pos.z - 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y, quad_pos.z - 0.5), current_frame),
                                                        block_types[self.get_block(x, y, z)].bottom_col
                                                        )

                        if (y == CHUNK_SIZE - 1 and ((self.position.x, self.position.y + 1, self.position.z) in world.chunks and world.chunks[(self.position.x, self.position.y + 1, self.position.z)].get_block(x, 0, z) == 0 or world.generate_block(Point3D(self.position.x * CHUNK_SIZE + x, (self.position.y + 1) * CHUNK_SIZE, self.position.z * CHUNK_SIZE + z)) == 0)) or (y != CHUNK_SIZE - 1 and self.get_block(x, y + 1, z) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x, CHUNK_SIZE * self.position.y + y + 0.5, CHUNK_SIZE * self.position.z + z)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y, quad_pos.z + 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y, quad_pos.z - 0.5), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y, quad_pos.z - 0.5), current_frame),
                                                        block_types[self.get_block(x, y, z)].top_col
                                                        )
    
                        if (z == 0 and ((self.position.x, self.position.y, self.position.z - 1) in world.chunks and world.chunks[(self.position.x, self.position.y, self.position.z - 1)].get_block(x, y, CHUNK_SIZE - 1) == 0 or world.generate_block(Point3D(self.position.x * CHUNK_SIZE + x, self.position.y * CHUNK_SIZE + y, (self.position.z - 1) * CHUNK_SIZE + CHUNK_SIZE - 1)) == 0)) or (z != 0 and self.get_block(x, y, z - 1) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x, CHUNK_SIZE * self.position.y + y, CHUNK_SIZE * self.position.z + z - 0.5)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y + 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y + 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y - 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y - 0.5, quad_pos.z), current_frame),
                                                        block_types[self.get_block(x, y, z)].side_col
                                                        )

                        if (z == CHUNK_SIZE - 1 and ((self.position.x, self.position.y, self.position.z + 1) in world.chunks and world.chunks[(self.position.x, self.position.y, self.position.z + 1)].get_block(x, y, 0) == 0 or world.generate_block(Point3D(self.position.x * CHUNK_SIZE + x, self.position.y * CHUNK_SIZE + y, (self.position.z + 1) * CHUNK_SIZE)) == 0)) or (z != CHUNK_SIZE - 1 and self.get_block(x, y, z + 1) == 0):
                            quad_pos = Point3D(CHUNK_SIZE * self.position.x + x, CHUNK_SIZE * self.position.y + y, CHUNK_SIZE * self.position.z + z + 0.5)
                            quads[quad_pos] = Convex_quad_3D(
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y + 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y + 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x - 0.5, quad_pos.y - 0.5, quad_pos.z), current_frame),
                                                        Point_to_project(Point3D(quad_pos.x + 0.5, quad_pos.y - 0.5, quad_pos.z), current_frame),
                                                        block_types[self.get_block(x, y, z)].side_col
                                                        )

        points: dict[Point3D, Point_to_project] = dict()

        for quad in quads.values():
            for index, point in enumerate(quad.points):
                if point.position_3D in points:
                    quad.points[index] = points[point.position_3D]
                else:
                    points[point.position_3D] = point


        self.quads = quads      
    
    def get_block(self, x, y, z):
        return self.blocks[x][y][z]

    def set_block(self, value, x, y, z):
        self.blocks[x][y][z] = value

class World:
    def __init__(self, seed: int = randint(0, 1000), render_distance = 2):
        self.seed = seed
        self.chunks: dict[tuple[int], Chunk] = {}
        self.main_terrain_scale = 0.05
        self.hill_terrain_scale = 0.01
        self.mountain_terrain_scale = 0.0005
        self.render_distance = render_distance
    
    def generate_chunk(self, point3D: Point3D, frame: int):
        chunk_to_add = Chunk(point3D)

        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    block_pos = point3D * CHUNK_SIZE + Point3D(x, y, z)
                    chunk_to_add.set_block(self.generate_block(block_pos), x, y, z)

        chunk_to_add.generate_quads(self, frame)
        
        return chunk_to_add

    def generate_necessary_chunks(self, camera_pos: Point3D, frame: int):
        current_chunk = Point3D(camera_pos.x // CHUNK_SIZE, camera_pos.y // CHUNK_SIZE, camera_pos.z // CHUNK_SIZE)

        n_chunks: dict[tuple[int], Chunk] = {}

        for x in range(-self.render_distance, self.render_distance + 1):
            for y in range(-self.render_distance, self.render_distance + 1):
                for z in range(-self.render_distance, self.render_distance + 1):
                    if sqrt(((x + current_chunk.x) * CHUNK_SIZE - (camera_pos.x - 4)) ** 2 + ((y + current_chunk.y) * CHUNK_SIZE - (camera_pos.y - 4)) ** 2 + ((z + current_chunk.z) * CHUNK_SIZE - (camera_pos.z - 4)) ** 2) <= self.render_distance * CHUNK_SIZE:
                        if (current_chunk.x + x, current_chunk.y + y, current_chunk.z + z) in self.chunks:
                            n_chunks[(current_chunk.x + x, current_chunk.y + y, current_chunk.z + z)] = self.chunks[(current_chunk.x + x, current_chunk.y + y, current_chunk.z + z)]
                        else:
                            n_chunks[(current_chunk.x + x, current_chunk.y + y, current_chunk.z + z)] = self.generate_chunk(Point3D(current_chunk.x + x, current_chunk.y + y, current_chunk.z + z), frame)
        
        self.chunks = n_chunks

    def generate_block(self, point3D: Point3D):
        return 1 if point3D.y < self.get_terrain_height_at_point(point3D) else 0

    def get_terrain_height_at_point(self, point3D: Point3D):
        detail_height = (noise.pnoise2(float(point3D.x * self.main_terrain_scale), float(point3D.z * self.main_terrain_scale), base=self.seed) + 1) * 5
        hill_height = ((noise.pnoise2(float(point3D.x * self.hill_terrain_scale), float(point3D.z * self.hill_terrain_scale), base=self.seed * 2) + 1) / 2) ** 0.75 * 15
        mountain_height = 5 ** ((noise.pnoise2(float(point3D.x * self.mountain_terrain_scale), float(point3D.z * self.mountain_terrain_scale), base=int(self.seed / 2)) + 1) / 2) * 100
        return detail_height + hill_height + mountain_height