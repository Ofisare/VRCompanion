import math

#*********************
# geometry operations 
#*********************
class Vector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

def subtract(v1, v2):
    return Vector(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def rotateYaw(v, angle):
    sin = math.sin(angle)
    cos = math.cos(angle)
    return Vector(cos * v.x - sin * v.z, v.y, sin * v.x + cos * v.z)

def dotProduct(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def crossProduct(a, b):
    return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y - b.x)
    
def angleBetween(a, b, n):
    dota = max(-1, min(1, dotProduct(a, b)))    
    dotn = max(-1, min(1, dotProduct(n, b)))    
    return math.atan2(dotn, dota)