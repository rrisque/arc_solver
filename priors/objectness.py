import json
import os

import numpy
from numpy import median


class Task:
    def __init__(self, name, task):
        self.name = name
        self.train = [Example(i) for i in task['train']]
        self.test = [Example(i) for i in task['test']]

    def __str__(self):
        return 'Task {} contains {} training examples.'.format(self.name, len(self.train))


class Example:
    def __init__(self, example):
        self.input = Scene(example['input'])
        self.output = Scene(example['output'])

    def __str__(self):
        return 'Input: {} \n' \
               'Maps to output {}'.format(self.input, self.output)


class Scene:
    def __init__(self, scene):
        self.scene = scene
        self.dimensions = [len(scene), len(scene[0])]
        self.size = self.dimensions[0] * self.dimensions[1]

    def __str__(self):
        return 'Scene of dimensions {}, size {}'.format(self.dimensions, self.size)

    def detect_objects(self):
        """
        Loops through entire scene, identifying objects based on color and spatial contiguity.
        :return: List of objects
        """
        objects = []
        array = self.scene

        for i in range(len(array)):
            for j in range(len(array[i])):
                # -1 represents already visited/owned spaces
                if array[i][j] != -1:
                    color = array[i][j]
                    new_point = Point(i, j, color)
                    new_object = Object(points=[new_point])
                    array[new_point.x][new_point.y] = -1

                    array = new_object.grow_object(array)
                    objects.append(new_object)

        return objects

    def denoise(self, tolerance=0):
        """
        Remove noise from the scene.
        :param tolerance: TODO
        """
        array = self.scene
        for i in range(len(array)):
            for j in range(len(array[i])):
                color = array[i][j]
                point = Point(i, j, color)
                neighbors = point.neighbors()
                neighbor_color = []
                for coords in neighbors:
                    if coords[0] < len(array) and coords[1] < len(array[0]):
                        neighbor_color.append(array[coords[0]][coords[1]])

                if tolerance == 0:
                    array[i][j] = median(neighbor_color)

        self.scene = array


class Point:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color

    def neighbors(self):
        """
        Calculate neighbors of a point. May return neighbors existing positively beyond scene scope.
        :return: List of neighbors (point coordinates).
        """
        neighbors = []
        for x in range(max(0, self.x - 1), self.x + 2):
            for y in range(max(0, self.y - 1), self.y + 2):
                if self.x != x or self.y != y:
                    neighbors.append([x, y])
        return neighbors


class Object:
    def __init__(self, points):
        self.points = points

    def __str__(self):
        return "Object of size {} is color {}.".format(self.size(), self.color())

    def size(self):
        return len(self.points)

    def color(self):
        return int(median([i.color for i in self.points]))

    # grow object based on both spatial contiguity and color
    def grow_object(self, array):
        """
        Grows an object based on color and spatial contiguity.
        :param array: Scene or subscene
        :return: Modified scene or subscene with "-1" put in any space now owned by this object.
        """
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


if __name__ == '__main__':
    training_dir = '../data/training/'
    for filename in os.listdir(training_dir):
        with open(training_dir + filename, 'r') as f:
            task = Task(filename, json.load(f))
        break

    task.train[1].input.detect_objects()

    scene = Scene(scene=numpy.array([[3, 3, 3, 3], [3, 0, 3, 3], [3, 3, 3, 3], [3, 3, 3, 0]]))
    print(scene)

    scene.denoise()
