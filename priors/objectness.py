import json
import os

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
        objects = []
        array = self.scene

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
                    objects.append(new_object)

        for object in objects:
            print(object)


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

    def __str__(self):
        return "Object of size {} is color {}.".format(self.size(), self.color())

    def size(self):
        return len(self.points)

    def color(self):
        return int(median([i.color for i in self.points]))

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


training_dir = '../data/training/'
for filename in os.listdir(training_dir):
    with open(training_dir + filename, 'r') as f:
        task = Task(filename, json.load(f))
    break

print(task)

for example in task.train:
    print(example)

task.train[0].input.detect_objects()
