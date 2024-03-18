import re
import fpdf
import argparse
import glob
import os
from tqdm import tqdm
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input directory with pngs")
parser.add_argument("-o", "--output", help="output pdf file")
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
pdf.set_author("A. Amini, A. Soleimany. MIT 6.S191")
pdf.set_margins(0, 0, 0)

# imagelist is the list with all image filenames
files = sorted(glob.glob(os.path.join(args.input, "*.jpeg")))
files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
import pdb; pdb.set_trace()
for image in tqdm(files):
    pdf.add_page()
    pdf.image(image, x=0, y=0, w=1280, h=720)
    if not args.no_watermark: 
        pdf.image("watermark.png", x=0, y=0, w=1280, h=720)

pdf.output(args.output, "F")
