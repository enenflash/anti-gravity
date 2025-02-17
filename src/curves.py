import math

def linear(x:float) -> float:
    return x

def ease_in(x:float, type:int=0) -> float:
    if type == 0: # parabola
        return x**2
    elif type == 1: # cubic
        return x**3
    elif type == 2: # hyperbola
        return 2/(x-2)-1
    
    return -math.cos(math.pi*x/2) + 1 # cosine

def ease_out(x, type:int=0) -> float:
    if type == 0: # parabola
        return -(x-1)**2+1
    elif type == 1: # cubic
        return (x-1)**3+1
    elif type == 2: # hyperbola
        return -(2/(x+1))+2
    
    return math.sin(math.pi*x/2) # sine

def ease(x, type=0) -> float:
    return 0.5*math.sin(math.pi * (x - 0.5)) + 0.5

def distort_out(x) -> float:
    return -0.3*math.sin((x-1)*math.pi*11.5)*(x-1)**3

def shockwave(x) -> float:
    return 0.4 * 9*x(3*x - 2)(x - 1)