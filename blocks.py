from positioning import *

class Block_type:
    """Container for basic data of a block type"""
    def __init__(self, top_col, side_col, bottom_col):
        self.top_col: int = top_col
        self.side_col: int = side_col
        self.bottom_col: int = bottom_col

block_types = {
    1: Block_type(3, 4, 4),
    2: Block_type(4, 4, 4),
    3: Block_type(13, 13, 13)
}

class Block:
    """Container for basic data of a block in the world"""
    def __init__(self, block_position: Point3D, type: Block_type):
        self.position: Point3D = block_position
        self.type = type