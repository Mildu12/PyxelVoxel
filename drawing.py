import pyxel
from positioning import *
from math import tan, copysign, radians, sqrt

def sign(x):
    return copysign(1, x)

def convex_quad(p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2, col: int, alpha: float = 1.0):
    """Points in clockwise order"""
    pyxel.dither(alpha)
    pyxel.tri(p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, col)
    pyxel.tri(p2.x, p2.y, p3.x, p3.y, p4.x, p4.y, col)
    pyxel.dither(1.0)

def convex_quad_b(p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2, col: int, alpha: float = 1.0):
    """Points in clockwise order"""
    pyxel.dither(alpha)
    pyxel.line(p1.x, p1.y, p2.x, p2.y, col)
    pyxel.line(p2.x, p2.y, p3.x, p3.y, col)
    pyxel.line(p3.x, p3.y, p4.x, p4.y, col)
    pyxel.line(p4.x, p4.y, p1.x, p1.y, col)
    
    pyxel.dither(1.0)

def convex_quad_and_b(p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2, col: int, colb: int = 0, alpha: float = 1.0):
    """Points in clockwise order"""

    convex_quad(p1, p2, p3, p4, col, alpha)
    convex_quad_b(p1, p2, p3, p4, colb, alpha)

class Block:
    def __init__(self, block_position: Vector3, top_col: int, side_col: int, bottom_col: int):
        self.position = block_position
        self.top_col = top_col
        self.side_col = side_col
        self.bottom_col = bottom_col

class Camera:
    def __init__(self, camera_position: Vector3, fov: float, screen_width, screen_height, pitch: float = 0.0, yaw: float = 0.0):
        self.position = camera_position
        self.fov = fov
        self.pitch = pitch
        self.yaw = yaw
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_fov = (self.fov / self.screen_width * self.screen_height)
        self.max_slope_x = tan(radians(90 - self.fov / 2.0))
        self.max_slope_y = tan(radians(90 - self.y_fov / 2.0))
        

    def draw_block(self, block: Block):
        position_diff = self.position - block.position
        
        if abs(position_diff.x) > 0.5:
            x_quad_pos = block.position.x + 0.5 * sign(position_diff.x)
            points = [self.project_point(Vector3(x_quad_pos, block.position.y + 0.5, block.position.z + 0.5)), self.project_point(Vector3(x_quad_pos, block.position.y + 0.5, block.position.z - 0.5)), self.project_point(Vector3(x_quad_pos, block.position.y - 0.5, block.position.z - 0.5)), self.project_point(Vector3(x_quad_pos, block.position.y - 0.5, block.position.z + 0.5))]
            
            works = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    works = True
                    break

            if works:
                convex_quad_and_b(points[0], points[1], points[2], points[3], block.side_col)

        if abs(position_diff.y) > 0.5:
            y_quad_pos = block.position.y + 0.5 * sign(position_diff.y)
        
            points = [self.project_point(Vector3(block.position.x + 0.5, y_quad_pos, block.position.z + 0.5)), self.project_point(Vector3(block.position.x + 0.5, y_quad_pos, block.position.z - 0.5)), self.project_point(Vector3(block.position.x - 0.5, y_quad_pos, block.position.z - 0.5)), self.project_point(Vector3(block.position.x - 0.5, y_quad_pos, block.position.z + 0.5))]
            
            works = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    works = True
                    break

            if works:
                if sign(position_diff.y) > 0:
                    convex_quad_and_b(points[0], points[1], points[2], points[3], block.top_col)
                else:
                    convex_quad_and_b(points[0], points[1], points[2], points[3], block.bottom_col)
            
        if abs(position_diff.z) > 0.5:
            z_quad_pos = block.position.z + 0.5 * sign(position_diff.z)
            points = [self.project_point(Vector3(block.position.x + 0.5, block.position.y + 0.5, z_quad_pos)), self.project_point(Vector3(block.position.x + 0.5, block.position.y - 0.5, z_quad_pos)), self.project_point(Vector3(block.position.x - 0.5, block.position.y - 0.5, z_quad_pos)), self.project_point(Vector3(block.position.x - 0.5, block.position.y + 0.5, z_quad_pos))]
            
            works = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    works = True
                    break

            if works:
                convex_quad_and_b(points[0], points[1], points[2], points[3], block.side_col)

    def project_point(self, point: Vector3) -> Vector2:
        rotated_point = self.rotate_point_around_self(point, self.pitch, self.yaw)
        
        slope_x = (rotated_point.x / abs(rotated_point.z))
        slope_y = (rotated_point.y / abs(rotated_point.z))
        
        pixel_pos = Vector2(slope_x / self.max_slope_x * self.screen_width + self.screen_width / 2, slope_y / self.max_slope_y * self.screen_height * 2 + self.screen_height / 2)

        return pixel_pos

    def rotate_point_around_self(self, point: Vector3, pitch_to_rotate: float, yaw_to_rotate: float) -> Vector3:
        position_diff = point - self.position
        
        yaw = pyxel.atan2(position_diff.z, position_diff.x)
    
        xz_dist = sqrt(position_diff.x ** 2 + position_diff.z ** 2) 
 
        rotated_point = Vector3(xz_dist * pyxel.cos(yaw - yaw_to_rotate), position_diff.y, xz_dist * pyxel.sin(yaw - yaw_to_rotate))
        
        yz_dist = sqrt(rotated_point.y ** 2 + rotated_point.z ** 2) 
        pitch = -pyxel.atan2(rotated_point.y, rotated_point.z)
        
        rotated_point = Vector3(rotated_point.x, yz_dist * pyxel.sin(pitch - pitch_to_rotate), yz_dist * pyxel.cos(pitch - pitch_to_rotate))

        return rotated_point

    def rotate(self, pitch_rotation, yaw_rotation):
        self.pitch += pitch_rotation
        self.yaw += yaw_rotation

        if self.yaw > 180:
            self.yaw = self.yaw - 360
        if self.yaw < -180:
            self.yaw = self.yaw + 360
        if self.pitch > 90:
            self.pitch = 90
        if self.pitch < -90:
            self.pitch = -90
