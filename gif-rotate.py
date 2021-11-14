#!/usr/bin/env python3

# python 3 script to spin an image on its y-axis
# or yz-axis by the specified number of degrees
# must specify input file, output file, and temporary
# directory to store images that make the animated gif
# ideal height and width can be omitted, but will default
# to the original image size
# rotation degrees can also be omitted, but will default
# to 360 degrees

# based on code from: https://github.com/eborboihuc/rotate_3d
# added code for arguments, working with the temp directory, gif optimizing & resizing, etc.

# todo:
# more error checking
# file handles

# Ken Mininger, kmininger@us.ibm.com
# October 2021

import argparse
from pygifsicle import gifsicle
import glob
import os
import shutil
import sys
import time
from pathlib import Path
from PIL import Image
from image_transformer import ImageTransformer
from util import save_image


# check the arguments
def check_args():
    parser = argparse.ArgumentParser(
        description="Rotates an image on its x-axis or xz-axis.", prog="gif-rotate",
        usage="%(prog)s "
              "[options]")
    parser.add_argument("-i", help="Input file - The file you want to work with.",
                        required=True)
    parser.add_argument("-o", help="Output file - The animated gif.", required=True)
    parser.add_argument("-d", help="Output directory - Directory to hold the images used for making the gif.",
                        required=True)
    parser.add_argument("-r", help="Degrees to rotate. If omitted, will default to 360.", type=int)
    parser.add_argument("-w", help="Ideal width. If omitted, will default to original image width.", type=int)
    parser.add_argument("-g", help="Ideal height. If omitted, will default to original image height.", type=int)
    parser.add_argument("-t", help="Type of rotation (y for y-axis, z for yz-axis). Omitted or invalid entry defaults "
                                   "to y.")
    args1 = parser.parse_args()
    return (args1)


# check that necessary arguments are supplied
def error_check(infile, outfile, directory):
    if not infile:
        print("Input file not provided: use -i")
        exit(1)
    if not os.path.isfile(infile):
        print("Input file not found")
        exit(1)
    if not outfile:
        print("Output file not provided: use -o")
        exit(1)
    if not directory:
        print("Output directory not provided: use -d")
        exit(1)


def make_gif(outfile, outdir):
    # create frames
    frames = []
    imgs = glob.glob(outdir + "\\*.jpg")

    # adding this to only save every 4 frames
    # for a 360 degree rotation this reduces
    # frames to 90 for filesize considerations
    skip = 1
    for i in imgs:
        new_frame = Image.open(i)
        if (skip % 4) == 0:
            frames.append(new_frame)
        skip += 1

    # save the rotating gif
    try:
        frames[0].save(outfile, format='GIF', append_images=frames[1:], save_all=True, duration=50, loop=0)
        print("GIF created:", outfile)
    except IOError:
        print("Error: Cannot open output file.")
        exit(1)

    # use gifsicle to reduce and optimize the animated gif, suppressing warning messages
    # this should get it to under 128kb
    # if not, the scale= value can be decreased until the desired filesize is reached
    gifsicle(sources=[outfile], destination=outfile, optimize=True, options=['--scale=0.7', '-w'])


# main
def main():
    # get args
    (args) = check_args()

    # set some variables
    outdir = str(args.d)
    outfile = str(args.o)
    img_path = args.i
    img_type = args.t
    rotation = args.r
    ideal_w = args.w
    ideal_h = args.g

    # check args
    error_check(img_path, outfile, outdir)

    # rotation
    rot_range = 360 if not rotation else int(rotation)

    # ideal width and height
    img_shape = None if (not ideal_w) or (not ideal_h) else (int(ideal_w), int(ideal_h))

    # where the magic happens
    it = ImageTransformer(img_path, img_shape)

    # create output directory
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if img_type is None:
        img_type = "y"

    if img_type == "y":
        for ang in range(0, rot_range):
            # rotate the image along the y-axis from 0 to specified degrees
            rotated_img = it.rotate_along_axis(phi=ang, dx=5)
            # save the gif
            save_image(outdir + '/{}.jpg'.format(str(ang).zfill(3)), rotated_img)
    else:
        for ang in range(0, rot_range):
            # rotate the image along the yz-axis from 0 to specified degrees
            rotated_img = it.rotate_along_axis(phi=ang, gamma=ang)
            # save the gif
            save_image(outdir + '/{}.jpg'.format(str(ang).zfill(3)), rotated_img)

    # the following can be used to rotate along the z-axis
    # rotated_img = it.rotate_along_axis(gamma = ang)

    make_gif(outfile, outdir)

    # need this to let the file handles close
    print("Sleeping for 30 seconds to give the file handles a chance to close.")
    time.sleep(30)

    # clean up the temp directory and images that make up the gif
    print("Cleaning up the output directory.")

    for files in os.listdir(outdir):
        path = os.path.join(outdir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    print("Done.")


if __name__ == '__main__':
    main()
