import pyxel
from src.positioning import *
from math import tan, radians, sqrt
from src.world_data import *
from src.blocks import *
from time import time

def sign(x) -> int:
    """Returns 1 if x >= 0 and -1 if x < 0"""
    return 1 if x >= 0 else -1

class Line_to_draw:
    def __init__(self, p1: Point2D, p2: Point2D, col: int):
        self.p1 = p1
        self.p2 = p2
        self.col = col
    
    def draw(self):
        pyxel.line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.col)
    
    def __hash__(self):
        hash(self.p1, self.p2)

class Convex_quad:
    def __init__(self, position_3D: Point3D, p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D, col: int, colb: int = 0):
        self.position_3D: Point3D = position_3D
        self.p1: Point2D = p1
        self.p2: Point2D = p2
        self.p3: Point2D = p3
        self.p4: Point2D = p4
        self.col: int = col
        self.colb: int = colb

    def draw_filled(self, alpha: float = 1.0):
        """
        Draws a filled-in convex quadrilateral
        Points in clockwise order
        """
        #Divides the quadrilateral into two triangles and draws the two triangles
        pyxel.dither(alpha)
        pyxel.tri(self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.p4.x, self.p4.y, self.col)
        pyxel.tri(self.p2.x, self.p2.y, self.p3.x, self.p3.y, self.p4.x, self.p4.y, self.col)
        pyxel.dither(1.0)

    def draw_border(self):
        """
        Draws a 1 pixel thick border of the convex quadrilateral 
        Points in clockwise order
        """
        #Draws all 4 sides one by one as lines
        pyxel.line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, self.colb)
        pyxel.line(self.p2.x, self.p2.y, self.p3.x, self.p3.y, self.colb)
        pyxel.line(self.p3.x, self.p3.y, self.p4.x, self.p4.y, self.colb)
        pyxel.line(self.p4.x, self.p4.y, self.p1.x, self.p1.y, self.colb)

    def draw_filled_and_border(self, alpha: float = 1.0):
        """
        Combination of convex_quad and convex_quad_border
        Points in clockwise order
        """

        self.draw_filled(alpha)
        self.draw_border()
    
    def is_visible(self, screen_size: Point2D) -> bool:
        points: list[Point2D] = [self.p1, self.p2, self.p3, self.p4]

        visible: bool = False

        for i in points:
            if i.x >= 0 and i.x < screen_size.x and i.y >= 0 and i.y < screen_size.y:
                visible = True
                break
        
        return visible

class Camera:
    """Handles drawing of all 3D elements onto the screen"""
    def __init__(self, camera_position: Point3D, fov: float, screen_width: int, screen_height: int, render_distance: int, bg_col: int = 6, pitch: float = 0.0, yaw: float = 0.0):
        self.position: Point3D = camera_position
        self.pitch: float = pitch
        self.yaw: float = yaw
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.render_distance = render_distance
        self.bg = bg_col

        self.fov: float
        self.y_fov: float
        self.min_slope_x: float
        self.min_slope_y: float

        self.change_fov(fov)

        self.quads_to_draw: list[Convex_quad] = []

    def project_point_onto_screen(self, point: Point3D) -> Point2D:
        rotated_point: Point3D = self.rotate_point_around_self(point, self.pitch, self.yaw) #The point, rotated so that its position is relative to the direction of the camera
        relative_rotated_point: Point3D = rotated_point - self.position #The point, relative to both the camera's rotation and position
        
        slope_x: float = (relative_rotated_point.x / abs(relative_rotated_point.z)) if relative_rotated_point.z != 0 else (relative_rotated_point.x / 0.1) #The slope of the point relative to the camera in the x direction
        slope_y: float = (relative_rotated_point.y / abs(relative_rotated_point.z)) if relative_rotated_point.z != 0 else (relative_rotated_point.y / 0.1) #The slope of the point relative to the camera in the x direction
        
        projected_point: Point2D = Point2D(slope_x / self.min_slope_x * self.screen_width + self.screen_width / 2, 
                                           slope_y / self.min_slope_y * self.screen_height * 2 + self.screen_height / 2) 
        

        if relative_rotated_point.z < 0:
            return Point2D(-10, -10)
        
        #The position of the point on the screen, calculated using the fact that the slope of a point relative to the camera is proportional to its position on screen
        
        return projected_point

    def rotate_point_around_self(self, point: Point3D, pitch_to_rotate: float, yaw_to_rotate: float) -> Point3D:
        relative_position: Point3D = point - self.position #The point, relative to the camera's position
        
        point_yaw = pyxel.atan2(relative_position.z, relative_position.x) #The yaw of the point relative to the camera
        xz_dist = sqrt(relative_position.x ** 2 + relative_position.z ** 2) #The distance on the xz plane between the point and the camera
 
        relative_rotated_point = Point3D(xz_dist * pyxel.cos(point_yaw - yaw_to_rotate), 
                                relative_position.y, 
                                xz_dist * pyxel.sin(point_yaw - yaw_to_rotate)) #Applies the desired yaw rotation on the relative point

        point_pitch = -pyxel.atan2(relative_rotated_point.y, relative_rotated_point.z) #The pitch of the yaw-rotated point relative to the camera. Negated because Pyxel has a flipped y-axis
        yz_dist = sqrt(relative_rotated_point.y ** 2 + relative_rotated_point.z ** 2) #The distance on the yz plane between the yaw-rotated point and the camera

        relative_rotated_point = Point3D(relative_rotated_point.x, 
                                yz_dist * pyxel.sin(point_pitch - pitch_to_rotate), 
                                yz_dist * pyxel.cos(point_pitch - pitch_to_rotate)) #Applies the desired pitch rotation on the relative point
        
        rotated_point = relative_rotated_point + self.position #Converts the point's position from relative to absolute

        return rotated_point

    def gather_quads_from_chunk(self, chunk: Chunk, current_frame: int):
        for key in chunk.quads:
            points = []
            quad = chunk.quads[key]
            for i in quad.points:
                if i.current_frame != current_frame + 1:
                    i.projected_position = self.project_point_onto_screen(i.position_3D)
                    i.current_frame = current_frame + 1
                points.append(i.projected_position)


            quad_2D = Convex_quad(key, points[0], points[1], points[2], points[3], quad.col)

            if quad.selected:
                quad_2D.colb = 10

            self.quads_to_draw.append(quad_2D)

    def quad_distance_to_self(self, quad: Convex_quad):
        if quad.colb == 0:
            return quad.position_3D.distance_to(self.position)
        else:
            return quad.position_3D.distance_to(self.position) - 0.75

    def filter_quads(self):
        n_quads_to_draw: list[Convex_quad] = []
        for i in self.quads_to_draw:
            if i.is_visible(Point2D(self.screen_width, self.screen_height)):
                n_quads_to_draw.append(i)

        self.quads_to_draw = n_quads_to_draw
        
    def sort_quads(self):
        self.quads_to_draw.sort(key=self.quad_distance_to_self, reverse=True)

    def draw_all_quads(self):
        st = time()
        for i in self.quads_to_draw:
            alpha = -0.125 * i.position_3D.distance_to(self.position) + self.render_distance - 0.5

            if alpha > 1:
                i.draw_filled_and_border()
            else:
                i.draw_filled(alpha)
        self.quads_to_draw = []

    def quad_is_on_screen(self, p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D) -> bool:
        quad_is_visible: bool = False
        for i in [p1, p2, p3, p4]:
            if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                quad_is_visible = True
                break
        
        return quad_is_visible

    def rotate(self, pitch_rotation, yaw_rotation):
        """
        Rotates the camera while making sure that the yaw is between -180 and 180 and that the pitch is between -90 and 90.
        Should be used instead of directly modifying the pitch and yaw values of the camera.
        """

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
    
    def change_fov(self, new_fov: float):
        self.fov: float = new_fov
        self.min_slope_x: float = tan(radians(self.fov / 2.0)) #The minimum slope a point can have relative to the camera and remain on screen in the x dimension
        self.min_slope_y: float = self.min_slope_x / self.screen_width * self.screen_height * 2 #The minimum slope a point can have relative to the camera and remain on screen in the y dimension

    def draw_world(self, world: World, current_frame: int):
        pyxel.cls(self.bg)
        for i in world.chunks:
            self.gather_quads_from_chunk(world.chunks[i], current_frame)
        self.filter_quads()
        self.sort_quads()
        self.draw_all_quads()