#!/usr/bin/env python

import numpy as np
import cv2
import sys
import os

# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = [];
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :
    
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )
    
    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in range(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask


# if __name__ == '__main__':
def main(file1, file2):
    filename1 = file1
    filename2 = file2
    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    points1 = readPoints(filename1.split(".")[0] + '.txt')
    points2 = readPoints(filename2.split(".")[0] + '.txt')

    output_image = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}"

    # Create directory if it doesn't exist
    output_dir = 'image'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(11):
        alpha = i / 10.0
        points = []
        for j in range(len(points1)):
            x = (1 - alpha) * points1[j][0] + alpha * points2[j][0]
            y = (1 - alpha) * points1[j][1] + alpha * points2[j][1]
            points.append((x, y))

        imgMorph = np.zeros(img1.shape, dtype=img1.dtype)

        with open("tri.txt") as file:
            for line in file:
                x, y, z = line.split()
                x = int(x)
                y = int(y)
                z = int(z)

                t1 = [points1[x], points1[y], points1[z]]
                t2 = [points2[x], points2[y], points2[z]]
                t = [points[x], points[y], points[z]]

                morphTriangle(img1, img2, imgMorph, t1, t2, t, alpha)

        # Save the morphed image
        output_filename = os.path.join(output_dir, '{}_{:03d}.jpg'.format(output_image,i))
        cv2.imwrite(output_filename, imgMorph)