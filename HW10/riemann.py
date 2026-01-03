import itertools
import numpy as np

def riemann_integral(f, bounds, partitions):
   
    n = len(bounds)  # number of variables
    deltas = [(b - a) / p for (a, b), p in zip(bounds, partitions)]  # step sizes
    
    # Generate all midpoints in the grid
    grids = []
    for (a, b), p, delta in zip(bounds, partitions, deltas):
        # Midpoints of subintervals
        grids.append([a + (i + 0.5) * delta for i in range(p)])
    
    # Cartesian product to get all points in n-dimensional grid
    points = itertools.product(*grids)
    
    # Sum over all points
    integral = 0.0
    for point in points:
        volume_element = np.prod(deltas)
        integral += f(*point) * volume_element
    
    return integral

# ---------------- Example ----------------
if __name__ == "__main__":
    # Example: f(x, y, z) = x + y + z over [0,1]^3
    f = lambda x, y, z: x + y + z
    bounds = [(0, 1), (0, 1), (0, 1)]  # 3D cube
    partitions = [10, 10, 10]           # 10 subdivisions per dimension
    
    result = riemann_integral(f, bounds, partitions)
    print(f"Approximate integral: {result}")
