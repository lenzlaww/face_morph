import dlib
import cv2
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def detectFace(string):
    img = cv2.imread(string)

    dets = detector(img, 1)

    for k, d in enumerate(dets):
        print("dets{}".format(d))
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))

        # 使用predictor进行人脸关键点识别 shape为返回的结果
        shape = predictor(img, d)
        
        # Get the image dimensions
        height, width, _ = img.shape
        
        # Add corners of the image as corresponding points
        corners = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        
        # Calculate halfway points between corners
        halfway_points = [((corners[i][0] + corners[j][0]) // 2, (corners[i][1] + corners[j][1]) // 2) 
                          for i in range(len(corners)) for j in range(i+1, len(corners))]
        
        # Combine facial landmarks with corners and halfway points
        all_points = list(shape.parts()) + corners + halfway_points

        # 绘制特征点
        output_filename = os.path.splitext(string)[0] + '.txt'

        with open(output_filename, 'w') as f:
            for pt in all_points:
                # Check if the point is a facial landmark or a corner/halfway point
                if hasattr(pt, 'x'):
                    # If it's a facial landmark, use pt.x and pt.y
                    f.write('{} {}\n'.format(pt.x, pt.y))
                    # Draw circle on the image
                    pt_pos = (int(pt.x), int(pt.y))
                    cv2.circle(img, pt_pos, 1, (255, 0, 0), 2)
                else:
                    # If it's a corner/halfway point, use tuple unpacking
                    f.write('{} {}\n'.format(pt[0], pt[1]))
                    # Draw circle on the image
                    cv2.circle(img, pt, 1, (255, 0, 0), 2)

    # cv2.imshow('img', img)
    # k = cv2.waitKey(500)
    # cv2.destroyAllWindows()

# if __name__ == '__main__':
#     detectFace('hillary_clinton.jpg')
#     detectFace('ted_cruz.jpg')
