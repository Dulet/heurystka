import numpy
import matplotlib.pyplot as plt
from values import values
from geopy import distance

distance = [[round(((distance.distance(tuple(x[:2]), tuple(y[:2]))).km)) for y in values] for x in values]

class Coordinate:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

def get_total_distance(coords):
    dist = 0
    for first, second in zip(coords[:-1], coords[1:]):
        dist += distance[first.index][second.index]
    dist += distance[coords[0].index][coords[-1].index]
    return dist

def plot(ax, coords):
    for first, second in zip(coords[:-1], coords[1:]):
        ax.plot([first.x, second.x], [first.y, second.y], 'b')
    ax.plot([coords[0].x, coords[-1].x], [coords[0].y, coords[-1].y], "b")
    for c in coords:
        ax.plot(c.x, c.y, 'ro')

if __name__ == "__main__":
    coords = []
    for i, value in enumerate(values):
        coords.append(Coordinate(value[0], value[1], i))

    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    plot(ax1, coords)

    T = 30
    FACTOR = 0.99
    T_INIT = T
    MAX_EPOCH = 100
    MAX_TRIES = 100
    VEHICLES = 5
    MAX_CAPACITY = 1000

    min_cost = get_total_distance(coords)

    for i in range(MAX_EPOCH):
        print(i, 'cost=', min_cost)
        T *= FACTOR
        for j in range(MAX_TRIES):
            r1, r2 = numpy.random.randint(0, len(coords), size=2)
            coords[r1], coords[r2] = coords[r2], coords[r1]
            new_cost = get_total_distance(coords)

            if new_cost < min_cost or (numpy.random.uniform() < numpy.exp((min_cost - new_cost) / T)):
                min_cost = new_cost
            else:
                coords[r1], coords[r2] = coords[r2], coords[r1]

    ax2 = fig.add_subplot(122)
    plot(ax2, coords)
    plt.show()