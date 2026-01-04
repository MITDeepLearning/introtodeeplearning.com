import re
import fpdf
import argparse
import glob
import os
from tqdm import tqdm
import cv2
import numpy as np
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input directory with pngs")
parser.add_argument("-o", "--output", help="output pdf file")
parser.add_argument("--quality", type=int, default=40, help="quality of the images")
parser.add_argument("--no-watermark", action='store_true', help="dont include a watermark")
args = parser.parse_args()

# def get_most_common_color(img):
#     return np.array([255, 255, 255])
#
# def remove_color(image, color):
#     channel_mask = [((image[:,:,i]==color[i])) for i in range(3)]
#     mask = 255*(1-np.prod(channel_mask, axis=0)[:,:,np.newaxis])
#
#     rgba = np.concatenate((image, mask), axis=2)
#     return rgba
#
#
# for image in tqdm(glob.glob(os.path.join(args.input, "*.png"))):
#     data = cv2.imread(image)
#     # background_color = get_most_common_color(data)
#     # rgba = remove_color(data, background_color)
#     cv2.imwrite(image+".comp.png", data, [cv2.IMWRITE_PNG_COMPRESSION, 9])

pdf = fpdf.FPDF(format=(1280, 720))
pdf.set_author("A. Amini, A.P. Amini. MIT 6.S191")
pdf.set_margins(0, 0, 0)

if not args.no_watermark:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    watermark_path = os.path.join(script_dir, "watermark.png")
    watermark_rgba = cv2.imread(watermark_path, cv2.IMREAD_UNCHANGED)
    if watermark_rgba is None:
        raise FileNotFoundError(f"Could not load watermark from {watermark_path}")
    
    # Extract alpha channel (we'll use this as the watermark pattern)
    if watermark_rgba.shape[2] == 4:
        watermark_alpha = watermark_rgba[:, :, 3]
    else:
        # If no alpha channel, use grayscale as pattern
        watermark_alpha = cv2.cvtColor(watermark_rgba, cv2.COLOR_BGR2GRAY)

# imagelist is the list with all image filenames
files = sorted(glob.glob(os.path.join(args.input, "*.jpeg")))
files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
import pdb; pdb.set_trace()
for image in tqdm(files):
    pdf.add_page()
    image_data = cv2.imread(image)

    if not args.no_watermark:
        # Calculate median brightness of the slide (normalized to 0-1)
        gray_slide = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        median_brightness = np.median(gray_slide) / 255.0
        
        # Resize watermark alpha to match the slide dimensions
        watermark_resized = cv2.resize(watermark_alpha, (image_data.shape[1], image_data.shape[0]))
        
        # Choose watermark color based on slide brightness
        if median_brightness < 0.5:
            # Dark slide -> add white watermark
            watermark_color = cv2.cvtColor(watermark_resized, cv2.COLOR_GRAY2BGR)
            image_data = cv2.addWeighted(image_data, 1, watermark_color, 1.2, 0)
        else:
            # Light slide -> subtract black watermark
            watermark_color = cv2.cvtColor(watermark_resized, cv2.COLOR_GRAY2BGR)
            # Subtract the watermark (makes it darker where watermark exists)
            image_data = cv2.subtract(image_data, (watermark_color * 1.2).astype(np.uint8))

    temp_file = tempfile.mktemp() + ".jpg"
    cv2.imwrite(temp_file, image_data, [int(cv2.IMWRITE_JPEG_QUALITY), args.quality])
    pdf.image(temp_file, x=0, y=0, w=1280, h=720)
    os.remove(temp_file)

pdf.output(args.output, "F")
