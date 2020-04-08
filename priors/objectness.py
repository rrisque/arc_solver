import json
import os

import numpy

from utils.utils import plot_task


class Point:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def neighbors(self):
        neighbors = []
        for x in range(max(0, self.x - 1), self.x + 2):
            for y in range(max(0, self.y - 1), self.y + 2):
                if self.x != x or self.y != y:
                    neighbors.append([x, y])
        return neighbors


class Object:
    def __init__(self, points):
        self.points = points

    # grow object based on both spatial contiguity and color
    def grow_object(self, array):
        # consider all points in the current object
        for point in self.points:
            neighbors = point.neighbors()
            for coords in neighbors:
                if coords[0] < len(array) and coords[1] < len(array[0]):
                    neighbor = Point(coords[0], coords[1], array[coords[0]][coords[1]])
                    # if neighbor doesn't belong to another group
                    if neighbor.color != -1:
                        # if neighbor is the same color as point
                        if neighbor.color == point.color:
                            # add point to object group and set to -1 in original array
                            self.points.append(neighbor)
                            array[neighbor.x][neighbor.y] = -1

        return array


def detect_objects_color(task):
    objects = []
    points = []
    array = numpy.asarray(task['test'][0]['input'])

    print(array)

    for i in range(len(array)):
        for j in range(len(array[i])):
            # -1 represents already visited/owned spaces
            if array[i][j] != -1:
                color = array[i][j]
                new_point = Point(i, j, color)
                new_object = Object(points=[new_point])
                array[new_point.x][new_point.y] = -1

                array = new_object.grow_object(array)

                print(array)
                objects.append(new_object)

    for object in objects:
        print(object)


training_dir = '../data/training/'
tasks = []
for filename in os.listdir(training_dir):
    with open(training_dir + filename, 'r') as f:
        tasks.append(json.load(f))


plot_task(tasks[0])

detect_objects_color(tasks[0])
