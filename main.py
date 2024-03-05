import argparse
import detectFace
import delaunay
import FaceMorph
import video


def main(file1, file2):
    # Detect faces in the images
    detectFace.detectFace(file1)
    detectFace.detectFace(file2)

    # Perform Delaunay triangulation
    delaunay.delaunay_tri(file1.split(".")[0] + '.txt', file2.split(".")[0] + '.txt')

    # Perform face morphing
    FaceMorph.main(file1, file2)

    # Create video
    video.makeVideo(file1, file2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face morphing script')
    parser.add_argument('arg1', type=str, help='Path to the first image file')
    parser.add_argument('arg2', type=str, help='Path to the second image file')
    args = parser.parse_args()

    main(args.arg1, args.arg2)
