import time
import argparse
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from utils import get_data

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output text file")
    parser.add_argument("--language", type=str, default="english")
    parser.add_argument("--mode", type=str, default="standard")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"],
                        help="background's color")
    parser.add_argument("--num_cols", type=int, default=300, help="number of character for output's width")
    parser.add_argument("--scale", type=int, default=2, help="upsize output")
    args = parser.parse_args()
    return args

def main(opt):
    start_time = time.time()
    
    if opt.background == "white":
        bg_code = (255, 255, 255)
    else:
        bg_code = (0, 0, 0)
    char_list, font, sample_character, scale = get_data(opt.language, opt.mode)
    num_chars = len(char_list)
    num_cols = opt.num_cols
    
    image = Image.open(opt.input).convert("RGB")
    width, height = image.size

    char_bbox = font.getbbox(sample_character)
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]

    cell_width = width / opt.num_cols
    cell_height = (char_height / char_width) * cell_width
    num_rows = int(height / cell_height)
    
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    
    np_image = np.array(image)
    
    for i in range(num_rows):
        for j in range(num_cols):
            left = int(j * cell_width)
            top = int(i * cell_height)
            right = min(int((j + 1) * cell_width), width)
            bottom = min(int((i + 1) * cell_height), height)
            partial_image = np_image[top:bottom, left:right, :]
            
            partial_avg_color = np.mean(partial_image, axis=(0, 1)).astype(np.int32)
            partial_avg_color = tuple(partial_avg_color.tolist())
            char_index = int(np.mean(partial_image) * num_chars / 255)
            char = char_list[min(char_index, num_chars - 1)]
            
            draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)
    
    if opt.background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    
    out_image.save(opt.output)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time: ", elapsed_time, "seconds")

if __name__ == '__main__':
    opt = get_args()
    main(opt)
