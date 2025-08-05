import math

class Vector:
    def __init__(self, i:int, j:int) -> None:
        self.i = i
        self.j = j
    
    @property
    def magnitude(self) -> None:
        return (self.i**2 + self.j**2)**(1/2)
    
    @property
    def argument(self) -> None:
        """returned in radians"""
        return math.atan2(self.j, self.i)
    
    def __eq__ (self, vec:"Vector") -> bool:
        return (self.i==vec.i) and (self.j==vec.j)
    
    def __add__ (self, vec:"Vector") -> "Vector":
        return Vector(self.i+vec.i, self.j+vec.j)
    
    def __sub__ (self, vec:"Vector") -> "Vector":
        return Vector(self.i-vec.i, self.j-vec.j)
    
    def scale(self, scalar:int|float) -> "Vector":
        return Vector(self.i*scalar, self.j*scalar)