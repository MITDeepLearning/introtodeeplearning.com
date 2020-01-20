import fpdf
import argparse
import glob
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input directory with pngs")
parser.add_argument("-o", "--output", help="output pdf file")
args = parser.parse_args()


pdf = fpdf.FPDF(format=(1280,720))
pdf.set_author("A. Amini, A. Soleimany. MIT 6.S191")
pdf.set_margins(0,0,0)

# imagelist is the list with all image filenames
for image in tqdm(glob.glob(os.path.join(args.input, "*.png"))):
    pdf.add_page()
    pdf.image(image, x=0, y=0, w=1280, h=720)
    pdf.image("watermark.png", x=0, y=0, w=1280, h=720)
    
pdf.output(args.output, "F")

