from positioning import *
from blocks import *
from random import randint
        
CHUNK_SIZE = 8

class Chunk:
    """Container for a 8x8x8 group of blocks"""
    def __init__(self, chunk_position: Point3D):
        self.position = chunk_position
        self.blocks: list[list[list[int]]] = [[[1 for z in range(CHUNK_SIZE)] for y in range(CHUNK_SIZE)] for x in range(CHUNK_SIZE)]

    def get_block(self, x, y, z):
        return self.blocks[x][y][z]

    def set_block(self, value, x, y, z):
        self.blocks[x][y][z] = value

class World:
    def __init__(self, seed: int = randint(1, 10000)):
        self.seed = seed
        self.chunks: dict[Point3D, Chunk]
    
    def generate_chunk(self, Point3D):
        chunk_to_add = Chunk(Point3D)

        for x in CHUNK_SIZE:
            for y in CHUNK_SIZE:
                for z in CHUNK_SIZE:
                    block_pos = Point3D * CHUNK_SIZE + Point3D(x, y, z)
                    chunk_to_add.set_block(self.generate_block(block_pos))

    def generate_block(self, Point3D):
        return 1