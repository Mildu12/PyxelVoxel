from math import sqrt, copysign

class Point2D:
    """Class for representing positions, distances or sizes in 2d space."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance_to(self, other: "Point2D") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def round(self, inplace: bool = False):
        if inplace:
            self.x, self.y = round(self.x), round(self.y)
        else: 
            return Point2D(round(self.x), round(self.y))
        
    def __abs__(self) -> "Point3D":
       return Point2D(abs(self.x), abs(self.y))
    
    def clamp(self, other: "Point2D", ignore_sign: bool = True) -> "Point2D":
        if ignore_sign:
            return Point2D(self.x if abs(self.x) < other.x else copysign(other.x, self.x), self.y if abs(self.y) < other.y else copysign(other.y, self.y))
        return Point2D(self.x if self.x < other.x else other.x, self.y if self.y < other.y else other.y)
    
    def __add__(self, other: "Point2D") -> "Point2D":
        return Point2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Point2D") -> "Point2D":
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Point2D":
        return Point2D(self.x * other, self.y * other)

    def __div__(self, other: float) -> "Point2D":
        return Point2D(self.x / other, self.y / other)
    
    def __neg__(self) -> "Point2D":
        return Point2D(-self.x, -self.y)
    
    def __repr__(self) -> str:
        return f"Point2D: x = {self.x}, y = {self.y}"

    def __round__(self) -> "Point2D":
        return Point2D(round(self.x), round(self.y))

    def clone(self) -> "Point2D":
        return Point2D(self.x, self.y)
    
    from math import sqrt, copysign

class Point3D:
    """Class for representing positions, distances or sizes in 3d space."""

    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z
    
    def distance_to(self, other: "Point3D") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def round(self, inplace: bool = False):
        if inplace:
            self.x, self.y, self.z = round(self.x), round(self.y), round(self.z)
        else: 
            return Point3D(round(self.x), round(self.y), round(self.z))
        
    def __abs__(self) -> "Point3D":
       return Point3D(abs(self.x), abs(self.y), abs(self.z))
    
    def clamp(self, other: "Point3D", ignore_sign: bool = True) -> "Point3D":
        if ignore_sign:
            return Point3D(self.x if abs(self.x) < other.x else copysign(other.x, self.x), self.y if abs(self.y) < other.y else copysign(other.y, self.y), self.z if abs(self.z) < other.z else copysign(other.z, self.z))
        return Point3D(self.x if self.x < other.x else other.x, self.y if self.y < other.y else other.y, self.z if self.z < other.z else other.z)
    
    def __add__(self, other: "Point3D") -> "Point3D":
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: "Point3D") -> "Point3D":
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> "Point3D":
        return Point3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> "Point3D":
        return Point3D(self.x / other, self.y / other, self.z / other)
    
    def __neg__(self) -> "Point3D":
        return Point3D(-self.x, -self.y, -self.z)
    
    def __repr__(self) -> str:
        return f"Point3D: x = {self.x}, y = {self.y}, z = {self.z}"

    def __round__(self) -> "Point3D":
        return Point3D(round(self.x), round(self.y), round(self.z))

    def clone(self) -> "Point3D":
        return Point3D(self.x, self.y, self.z)