import argparse
# https://imageio.readthedocs.io/en/stable/examples.html
#import imageio as iio
import imageio.v2 as iio

from scipy import ndimage
import numpy as np
# https://www.nicolaromano.net/data-thoughts/scikit-image-pt-1/
#import skimage
import os


def load_image_from_file(filename):
    img = iio.imread(filename)
    return img


def save_image_to_file(img, filename):
    img = iio.imwrite(filename, img)


def crop_and_save(img, output_folder, player_name, start_stage):
    #STAGE_HEADER_COLOR = (0x88, 0x88, 0x88)
    #STAGE_BACK_COLOR = (0xEE, 0xEE, 0xEE)
    STAGE_HEADER_COLOR = 0x88
    STAGE_BACK_COLOR = 0xEE
    MAX_STAGE_HEIGHT = 275

    stage = start_stage

    img_height = img.shape[0]
    #img_width = img.shape[1]

    row = 0
    while row < img_height:
        imgrow = img[row]

        if (imgrow[0][0] == STAGE_HEADER_COLOR) and (imgrow[1][0] == STAGE_HEADER_COLOR): # Found start of stage header
            first_row = row
            stage_height = 0
            while (imgrow[0][0] == STAGE_HEADER_COLOR) and (imgrow[1][0] == STAGE_HEADER_COLOR): # While inside stage header, keep going
                row = row + 1
                imgrow = img[row]
            while (imgrow[0][0] == STAGE_BACK_COLOR) and (imgrow[1][0] == STAGE_BACK_COLOR): # Now we have found the stage info area, keep going until we reach next stage header
                row = row + 1
                stage_height = row - first_row
                if (stage_height > MAX_STAGE_HEIGHT):
                    break
                imgrow = img[row]
            last_row = row - 1
            print('Found stage {} at {} to {} with height = {}'.format(stage, first_row, last_row, stage_height))

            # Copy the stage data into a new bitmap
            stageimg = img[first_row:last_row]

            # Save it out
            output_file = os.path.normpath(os.path.join(output_folder, '{}_{}.png'.format(player_name, stage)))
            print(output_file)
            save_image_to_file(stageimg, output_file)
            stage = stage + 1
        else:
            row = row + 1

def test():
    # https://pillow.readthedocs.io/en/stable/reference/Image.html
    from PIL import Image
    photo = Image.open('C:/Temp/ttt.png') #your image
    photo = photo.convert('RGB')
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    width = photo.size[0] #define W and H
    height = photo.size[1]

    for y in range(0, height): #each pixel has coordinates
        row = ""
        for x in range(0, width):
            RGB = photo.getpixel((x,y))
            R,G,B = RGB  #now you can use the RGB value
            print(RGB)
            if (RGB == RED):
                print('red')
            if (RGB == GREEN):
                print('green')
            if (RGB == BLUE):
                print('blue')

def main():
    """Main Function"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--in-file', dest='input_file', required=True, help='Input filename')
    parser.add_argument('-o', '--out-folder', dest='output_folder', required=True, help='Output folder')
    parser.add_argument('-p', '--player-name', dest='player_name', required=True, help='Player name')
    parser.add_argument('-ss', '--start-stage', dest='start_stage', required=False, default=1, help='Player name')
    args = parser.parse_args()

    img = load_image_from_file(args.input_file)

    crop_and_save(img, args.output_folder, args.player_name, int(args.start_stage))


if __name__ == "__main__":
    main()
