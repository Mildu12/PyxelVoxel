from math import sqrt, copysign

class Vector2:
    """Class for representing positions, distances or sizes in 2d space."""

    def __init__(self, x: float, y: float):
        """
        x and y are the x and y coordonites of the Vector2
        """
        self.x = x
        self.y = y
    
    def distance_to(self, other: "Vector2") -> float:
        """Returns the distance between the two Vector2s"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def round(self, inplace: bool = False):
        """Equal to Vector2(round(self.x), round(self.y))"""
        if inplace:
            self.x, self.y = round(self.x), round(self.y)
        else: 
            return Vector2(round(self.x), round(self.y))
        
    def __abs__(self):
       
       return Vector2(abs(self.x), abs(self.y))
    
    def clamp(self, other: "Vector2", ignore_sign: bool = True) -> "Vector2":
        if ignore_sign:
            return Vector2(self.x if abs(self.x) < other.x else copysign(other.x, self.x), self.y if abs(self.y) < other.y else copysign(other.y, self.y))
        return Vector2(self.x if self.x < other.x else other.x, self.y if self.y < other.y else other.y)
    
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Vector2":
        return Vector2(self.x * other, self.y * other)

    def __div__(self, other: float) -> "Vector2":
        return Vector2(self.x / other, self.y / other)
    
    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)
    
    def __repr__(self) -> str:
        return f"Vector2: x = {self.x}, y = {self.y}"

    def __round__(self) -> "Vector2":
        return Vector2(round(self.x), round(self.y))

    def clone(self) -> "Vector2":
        return Vector2(self.x, self.y)
    
    from math import sqrt, copysign

class Vector3:
    """Class for representing positions, distances or sizes in 3d space."""

    def __init__(self, x: float, y: float, z:float):
        """
        x and y are the x and y coordonites of the Vector3
        """
        self.x = x
        self.y = y
        self.z = z
    
    def distance_to(self, other: "Vector3") -> float:
        """Returns the distance between the two Vector3s"""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def round(self, inplace: bool = False):
        """Equal to Vector3(round(self.x), round(self.y))"""
        if inplace:
            self.x, self.y, self.z = round(self.x), round(self.y), round(self.z)
        else: 
            return Vector3(round(self.x), round(self.y), round(self.z))
        
    def __abs__(self):
       return Vector3(abs(self.x), abs(self.y), abs(self.z))
    
    def clamp(self, other: "Vector3", ignore_sign: bool = True) -> "Vector3":
        if ignore_sign:
            return Vector3(self.x if abs(self.x) < other.x else copysign(other.x, self.x), self.y if abs(self.y) < other.y else copysign(other.y, self.y), self.z if abs(self.z) < other.z else copysign(other.z, self.z))
        return Vector3(self.x if self.x < other.x else other.x, self.y if self.y < other.y else other.y, self.z if self.z < other.z else other.z)
    
    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> "Vector3":
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other: float) -> "Vector3":
        return Vector3(self.x / other, self.y / other, self.z / other)
    
    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)
    
    def __repr__(self) -> str:
        return f"Vector3: x = {self.x}, y = {self.y}, z = {self.z}"

    def __round__(self) -> "Vector3":
        return Vector3(round(self.x), round(self.y), round(self.z))

    def clone(self) -> "Vector3":
        return Vector3(self.x, self.y, self.z)