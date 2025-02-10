import pyxel
from positioning import *
from math import tan, radians, sqrt

def sign(x) -> int:
    """Returns 1 if x >= 0 and -1 if x < 0"""
    return 1 if x >= 0 else -1

def convex_quad(p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D, col: int):
    """
    Draws a filled-in convex quadrilateral
    Points in clockwise order
    """
    #Divides the quadrilateral into two triangles and draws the two triangles
    pyxel.tri(p1.x, p1.y, p2.x, p2.y, p4.x, p4.y, col)
    pyxel.tri(p2.x, p2.y, p3.x, p3.y, p4.x, p4.y, col)

def convex_quad_border(p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D, col: int):
    """
    Draws a 1 pixel thick border of the convex quadrilateral 
    Points in clockwise order
    """
    #Draws all 4 sides one by one as lines
    pyxel.line(p1.x, p1.y, p2.x, p2.y, col)
    pyxel.line(p2.x, p2.y, p3.x, p3.y, col)
    pyxel.line(p3.x, p3.y, p4.x, p4.y, col)
    pyxel.line(p4.x, p4.y, p1.x, p1.y, col)

def convex_quad_with_border(p1: Point2D, p2: Point2D, p3: Point2D, p4: Point2D, col: int, colb: int = 0):
    """
    Combination of convex_quad and convex_quad_border
    Points in clockwise order
    """

    convex_quad(p1, p2, p3, p4, col)
    convex_quad_border(p1, p2, p3, p4, colb)

class Block:
    """Container for basic data of a block"""
    def __init__(self, block_position: Point3D, top_col: int, side_col: int, bottom_col: int):
        self.position = block_position
        self.top_col = top_col
        self.side_col = side_col
        self.bottom_col = bottom_col

class Camera:
    """Handles drawing of all 3D elements onto the screen"""
    def __init__(self, camera_position: Point3D, fov: float, screen_width, screen_height, pitch: float = 0.0, yaw: float = 0.0):
        self.position = camera_position
        self.fov = fov
        self.pitch = pitch
        self.yaw = yaw
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_fov = (self.fov / self.screen_width * self.screen_height) #Vertical FOV in degrees

        self.max_slope_x = tan(radians(90 - self.fov / 2.0)) #The maximum slope a point can have relative to the camera and remain on screen in the x dimension
        self.max_slope_y = tan(radians(90 - self.y_fov / 2.0)) #The maximum slope a point can have relative to the camera and remain on screen in the y dimension

    def draw_block(self, block: Block):
        relative_position: Point3D = self.position - block.position

        #Divides a cube into three quadrilaterals that we need to draw, one for each plane
        
        if abs(relative_position.x) > 0.5: #Checks if the quadrilateral on the yz plane is visible from the camera
        
            x_plane_pos: float = block.position.x + 0.5 * sign(relative_position.x) #The x position of the yz plane that the quadrilateral is on
            points: list[Point2D] = [self.project_point_onto_screen(Point3D(x_plane_pos, block.position.y + 0.5, block.position.z + 0.5)), 
                                     self.project_point_onto_screen(Point3D(x_plane_pos, block.position.y + 0.5, block.position.z - 0.5)), 
                                     self.project_point_onto_screen(Point3D(x_plane_pos, block.position.y - 0.5, block.position.z - 0.5)), 
                                     self.project_point_onto_screen(Point3D(x_plane_pos, block.position.y - 0.5, block.position.z + 0.5))] #The projetions onto the screen of the 4 points that make up the quadrilateral
            
            #Makes sure at least one of the quadrilateral's points are on screen (this method is not foolproof)
            quad_is_visible: bool = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    quad_is_visible = True
                    break

            if quad_is_visible:
                convex_quad_with_border(points[0], points[1], points[2], points[3], block.side_col)

        if abs(relative_position.y) > 0.5: #Checks if the quadrilateral on the xz plane is visible from the camera

            y_plane_pos: float = block.position.y + 0.5 * sign(relative_position.y) #The y position of the xz plane that the quadrilateral is on
            points: list[Point2D] = [self.project_point_onto_screen(Point3D(block.position.x + 0.5, y_plane_pos, block.position.z + 0.5)), 
                                     self.project_point_onto_screen(Point3D(block.position.x + 0.5, y_plane_pos, block.position.z - 0.5)), 
                                     self.project_point_onto_screen(Point3D(block.position.x - 0.5, y_plane_pos, block.position.z - 0.5)), 
                                     self.project_point_onto_screen(Point3D(block.position.x - 0.5, y_plane_pos, block.position.z + 0.5))] #The projetions onto the screen of the 4 points that make up the quadrilateral
            
            #Makes sure at least one of the quadrilateral's points are on screen (this method is not foolproof)
            quad_is_visible = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    quad_is_visible = True
                    break

            if quad_is_visible:
                #Checks whether the block's top color or bottom color should be displayed.
                if sign(relative_position.y) > 0:
                    convex_quad_with_border(points[0], points[1], points[2], points[3], block.top_col)
                else:
                    convex_quad_with_border(points[0], points[1], points[2], points[3], block.bottom_col)
            
        if abs(relative_position.z) > 0.5: #Checks if the quadrilateral on the xy plane is visible from the camera
    
            z_plane_pos: float = block.position.z + 0.5 * sign(relative_position.z) #The z position of the xy plane that the quadrilateral is on
            points: list[Point2D] = [self.project_point_onto_screen(Point3D(block.position.x + 0.5, block.position.y + 0.5, z_plane_pos)), 
                                     self.project_point_onto_screen(Point3D(block.position.x + 0.5, block.position.y - 0.5, z_plane_pos)), 
                                     self.project_point_onto_screen(Point3D(block.position.x - 0.5, block.position.y - 0.5, z_plane_pos)), 
                                     self.project_point_onto_screen(Point3D(block.position.x - 0.5, block.position.y + 0.5, z_plane_pos))] #The projetions onto the screen of the 4 points that make up the quadrilateral
            
            #Makes sure at least one of the quadrilateral's points are on screen (this method is not foolproof)
            quad_is_visible = False
            for i in points:
                if i.x >= 0 and i.x < self.screen_width and i.y >= 0 and i.y < self.screen_height:
                    quad_is_visible = True
                    break

            if quad_is_visible:
                convex_quad_with_border(points[0], points[1], points[2], points[3], block.side_col)

    def project_point_onto_screen(self, point: Point3D) -> Point2D:
        rotated_point: Point3D = self.rotate_point_around_self(point, self.pitch, self.yaw) #The point, rotated so that its position is relative to the direction of the camera
        relative_rotated_point: Point3D = rotated_point - self.position #The point, relative to both the camera's rotation and position
        
        slope_x: float = (relative_rotated_point.x / abs(relative_rotated_point.z)) #The slope of the point relative to the camera in the x direction
        slope_y: float = (relative_rotated_point.y / abs(relative_rotated_point.z)) #The slope of the point relative to the camera in the x direction
        
        projected_point: Point2D = Point2D(slope_x / self.max_slope_x * self.screen_width + self.screen_width / 2, 
                                           slope_y / self.max_slope_y * self.screen_height * 2 + self.screen_height / 2) 
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