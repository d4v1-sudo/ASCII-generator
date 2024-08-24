import time
import argparse
from PIL import Image
import numpy as np

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.txt", help="Path to output text file")
    parser.add_argument("--mode", type=str, default="simple", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--num_cols", type=int, default=150, help="number of character for output's width")
    args = parser.parse_args()
    return args

def main(opt):
    start_time = time.time()
    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    
    image = Image.open(opt.input).convert("L")
    width, height = image.size
    cell_width = width / opt.num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    # Convert the image to a numpy array once
    np_image = np.array(image)

    with open(opt.output, 'w') as output_file:
        for i in range(num_rows):
            for j in range(num_cols):
                left = j * cell_width
                top = i * cell_height
                right = (j + 1) * cell_width
                bottom = (i + 1) * cell_height
                # Avoid creating a new PIL Image object for each cell, use array slicing
                cell = np_image[int(top):int(bottom), int(left):int(right)]
                avg_luminance = int(np.mean(cell))
                # Calculate the index directly without scaling
                char_idx = min(int(avg_luminance * num_chars / 255), num_chars - 1)
                output_file.write(CHAR_LIST[char_idx])
            output_file.write("\n")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, "seconds")

if __name__ == '__main__':
    opt = get_args()
    main(opt)
