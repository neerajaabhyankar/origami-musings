"""code to create 4 linked closed curves using vedo library"""

import vedo
import numpy as np

#function to translate a set of points
def translate(points, x, y, z):
    # create a new list of points
    new_points = []
    # for each point in the list of points
    for point in points:
        # add the translated point to the list of new points
        new_points.append((point[0] + x, point[1] + y, point[2] + z))
    # return the list of new points
    return new_points

#function to rotate a set of points about a given axis around the mean of those points
def rotate(points, axis, angle):
    # create a new list of points
    new_points = []
    # find the mean of the points
    mean = np.mean(points, axis=0)
    # for each point in the list of points
    for point in points:
        # rotate the point about the mean and add it to the list of new points
        new_points.append(rotate_point(point, axis, angle, mean))
    # return the list of new points
    return new_points

#function to rotate a point about a given axis around a given point
def rotate_point(point, axis, angle, origin):
    # create a vector from the origin to the point
    vector = np.array(point) - np.array(origin)
    # create a rotation matrix
    rotation_matrix = create_rotation_matrix(axis, angle)
    # rotate the vector
    rotated_vector = np.dot(rotation_matrix, vector)
    # return the rotated vector plus the origin
    return rotated_vector + np.array(origin)

#function to create a rotation matrix
def create_rotation_matrix(axis, angle):
    # create a unit vector from the axis
    axis = axis / np.sqrt(np.dot(axis, axis))
    # create the rotation matrix
    rotation_matrix = np.cos(angle) * np.eye(3) + np.sin(angle) * np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]]) + (1 - np.cos(angle)) * np.outer(axis, axis)
    # return the rotation matrix
    return rotation_matrix


# create a closed curve with a segment between every adjacent pair of points and a segment between the last and first points
def create_curve(points, color):
    # add the first point to the end of the list of points
    points.append(points[0])

    # create the curve
    curve = vedo.shapes.Line(points, c=color, lw=20)
    # add a point to the curve
    # curve.pointSize(20).addPoint(points[0])
    # return the curve
    return curve

# provide the point set for first curve
points1 = [(0,0,0), (1,0,0), (1,1,0), (1,1,1), (0,1,1), (0,0,1)]

# provide the point set for second curve (translate the first curve) 
points2 = translate(points1, 2, 0, 0)

# provide the point set for third curve (rotate the first curve about the z-axis)
points3 = rotate(points1, (0,0,1), 45)

# provide the point set for fourth curve (rotate the first curve about the y-axis)
points4 = rotate(points1, (0,1,0), 45)

# create the curve
curve1 = create_curve(points1, 'red')
curve2 = create_curve(points2, 'blue')
curve3 = create_curve(points3, 'green')
curve4 = create_curve(points4, 'yellow')

#plot curve
vedo.show(curve1, curve2, curve3, curve4, __doc__, viewup='z', axes=1).close()
