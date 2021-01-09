# This file recognizes the inputted gesture and outputs it
import math
import numpy as np


def translate_gesture(gesture, x_set, y_set):
    translated = []
    for point in gesture:
        x, y = point[0] + x_set, point[1] + y_set
        point = [x, y]
        translated.append(point)
    return translated


def scale_gesture(gesture, x_scale, y_scale):
    scaled = []
    for point in gesture:
        x, y = point[0] * x_scale, point[1] * y_scale
        point = [x, y]
        scaled.append(point)
    return scaled


def get_box(gesture):
    x_points = []
    y_points = []
    for point in gesture:
        x_points.append(point[0])
        y_points.append(point[1])
    box = [[min(x_points), min(y_points)], [max(x_points), max(y_points)]]
    return box


def gesture_length(gesture):
    if len(gesture) <= 1:
        return 0
    dist = []
    this_item = gesture[0]
    for item in gesture:
        prev_item = np.array(this_item)
        this_item = np.array(item)
        coord_dist = np.linalg.norm(prev_item - this_item)
        dist.append(coord_dist)
    return sum(dist)


def get_points(gesture, lon):
    new_gest = []
    for i in lon:
        new_gest.append(gesture[i])
    return new_gest


def move_and_scale(gesture, x_scale, y_scale):
    box = get_box(gesture)
    min_x = box[0][0]
    min_y = box[0][1]
    translated = translate_gesture(gesture, -min_x, -min_y)
    return scale_gesture(translated, x_scale, y_scale)


def normalize(gesture):
    scaled = move_and_scale(gesture, 1, 1)
    box = get_box(scaled)
    max_x = box[1][0]
    max_y = box[1][1]
    if max_x >= 30 and max_y < 30:
        return move_and_scale(scaled, 200/max_x, 1)
    elif max_x < 30 and max_y >= 30:
        return move_and_scale(scaled, 1, 200/max_y)
    else:
        return move_and_scale(scaled, 200/max_x, 200/max_y)


def sub_sample(gesture, k):
    new_gest = []
    for i in range(k):
        if i == k-1:
            new_point = gesture[-1]
        else:
            new_point = gesture[math.floor(i*len(gesture)/(k-1))]
        new_gest.append(new_point)
    return new_gest


def geometric_match(gesture1, gesture2, k):
    gesture1 = normalize(sub_sample(gesture1, k))
    gesture2 = normalize(sub_sample(gesture2, k))
    values = []
    for i in range(k):
        p1 = gesture1[i]
        p2 = gesture2[i]
        distance = math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
        values.append(distance)
    return sum(values) / len(values)


def k_point_rec(gesture, template, k):
    all_distances = []
    for key in template.keys():

        dist = geometric_match(gesture, template[key], k)
        all_distances.append(dist)

    index = np.argmin(all_distances)
    keys = list(template)
    return keys[index]
