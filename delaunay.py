import numpy as np
from scipy.spatial import Delaunay


def delaunay_tri(file1, file2):
    # Read data from the two text files
    with open(file1, 'r') as file1, open(file2, 'r') as file2:
        data1 = np.loadtxt(file1)
        data2 = np.loadtxt(file2)

    # Calculate the average of corresponding points
    average_points = (data1 + data2) / 2

    # Perform Delaunay triangulation
    tri = Delaunay(average_points)

    # Save the triangulation points into a new file
    with open('tri.txt', 'w') as tri_file:
        for triangle in tri.simplices:
            tri_file.write('{} {} {}\n'.format(triangle[0], triangle[1], triangle[2]))
