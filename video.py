import cv2
import os

def makeVideo(file1, file2, output_filename=None):
    # Directory containing the images
    image_dir = "image/"

    # Get all image filenames with specific names
    output_image = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}"
    image_files = sorted([filename for filename in os.listdir(image_dir) if filename.startswith(output_image)])

    # Determine the width and height of the first image
    img = cv2.imread(os.path.join(image_dir, image_files[0]))
    height, width, _ = img.shape

    # Define the output filename
    if output_filename is None:
        output_filename = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}.mp4"

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change codec as per your requirement
    video_out = cv2.VideoWriter(output_filename, fourcc, 15.0, (width, height))

    # Write images to video
    for image_file in image_files:
        img = cv2.imread(os.path.join(image_dir, image_file))
        video_out.write(img)

    # Release VideoWriter
    video_out.release()