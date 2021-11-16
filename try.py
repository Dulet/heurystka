import numpy
import matplotlib.pyplot as plt
from values import values
from geopy import distance

# tworzenie listy dystansow miedzy kazdymi punktami
distance = [[round(((distance.distance(tuple(x[:2]), tuple(y[:2]))).km)) for y in values] for x in values] 

# wartości które możemy zmieniać
T = 30
FACTOR = 0.999
T_INIT = T
MAX_EPOCH = 1000
MAX_TRIES = 100
CAPACITY = 1000

class Coordinate:
    def __init__(self, x, y, capacity, index):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.index = index
        
    def __repr__(self):
        return self.index

# limit pojemności 
def into_vehicle_paths(coords):
    tempcoords = coords[1:]
    paths = [[coords[0]]]
    capacity = CAPACITY
    while tempcoords:
        if tempcoords[0].capacity > capacity:
            paths.append([coords[0]])
            capacity = CAPACITY
        else:
            capacity -= tempcoords[0].capacity
            paths[-1].append(tempcoords[0])
            tempcoords = tempcoords[1:]
    return paths

def get_total_distance(coords):
    dist = 0
    for first, second in zip(coords[:-1], coords[1:]):
        dist += distance[first.index][second.index]
    dist += distance[coords[0].index][coords[-1].index]
    return dist

def get_multiple_paths_distance(coords):
    return sum(get_total_distance(path) for path in into_vehicle_paths(coords))

# tworzenie scatterplota połączonych punktów
def plot(ax, coords):
    ax.set_title(f'Cost: {get_multiple_paths_distance(coords)}')
    for path, color in zip(into_vehicle_paths(coords), ['r', 'g', 'b', 'gold', 'violet']):
        for first, second in zip(path[:-1], path[1:]):
            ax.plot([first.x, second.x], [first.y, second.y], color)
        ax.plot([path[0].x, path[-1].x], [path[0].y, path[-1].y], color)
    for i, value in enumerate(values):
        ax.annotate(i, xy=(value[0], value[1]))
    for c in coords:
        ax.plot(c.x, c.y, 'ro')

if __name__ == "__main__":
    coords = []
    for i, value in enumerate(values):
        coords.append(Coordinate(value[0], value[1], value[2], i)) # przypisane koordynatów oraz zapotrzebowania

    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    plot(ax1, coords)

    min_cost = get_multiple_paths_distance(coords) # min dystans obliczany jako suma tras wszystkich pojazdów

    # wykorzystanie algorytmu wyżarzania 
    for i in range(MAX_EPOCH):
        print(f'{i} cost={min_cost}')
        T *= FACTOR
        for j in range(MAX_TRIES):
            r1, r2 = numpy.random.randint(1, len(coords), size=2)
            coords[r1], coords[r2] = coords[r2], coords[r1]
            new_cost = get_multiple_paths_distance(coords)

            if new_cost < min_cost or (numpy.random.uniform() < numpy.exp((min_cost - new_cost) / T)):
                min_cost = new_cost
            else:
                coords[r1], coords[r2] = coords[r2], coords[r1]

    for i, path in enumerate(into_vehicle_paths(coords)):
        print(f'Vehicle {i + 1}: {get_total_distance(path)}km, path: {" -> ".join(str(point.index) for point in path)}')
    print(f"Total length: {min_cost}km")
    
    ax2 = fig.add_subplot(122)
    plot(ax2, coords)
    plt.show()
