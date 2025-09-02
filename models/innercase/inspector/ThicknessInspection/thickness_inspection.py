import sys, os, datetime
import math

import cv2
import numpy as np
import argparse

pos01_X = 810;  pos01_Y = 114;  XY_1 = "_X-360Y360_"
pos02_X = 2040; pos02_Y = 234;  XY_2 = "_X000Y360_"
pos03_X = 3264; pos03_Y = 138;  XY_3 = "_X360Y360_"
pos04_X = 714;  pos04_Y = 1550; XY_4 = "_X-360Y000_"
pos05_X = 1878; pos05_Y = 1620; XY_5 = "_X000Y000_"
pos06_X = 3339; pos06_Y = 1595; XY_6 = "_X360Y000_"
pos07_X = 768;  pos07_Y = 2772; XY_7 = "_X-360Y-360_"
pos08_X = 2022; pos08_Y = 2793; XY_8 = "_X000Y-360_"
pos09_X = 3225; pos09_Y = 2739; XY_9 = "_X360Y-360_"

threshold = 170
threshold_centroid = 170
crop_size = 140; crop_size_half = int(crop_size/2)
scale = 8; scale_crop = 1.5

PASS_FAIL_THRESHOLD = [300, 300, 300, 300, 300, 300, 300, 300, 300]

def estimate_thickness(image_path:str) -> list[float]:
  data_thickness = []

  for i in range(9):
    if i == 0:
        pos_X = pos01_X; pos_Y = pos01_Y; XY_coor = XY_1
    elif i == 1:
        pos_X = pos02_X; pos_Y = pos02_Y; XY_coor = XY_2
    elif i == 2:
        pos_X = pos03_X; pos_Y = pos03_Y; XY_coor = XY_3
    elif i == 3:
        pos_X = pos04_X; pos_Y = pos04_Y; XY_coor = XY_4
    elif i == 4:
        pos_X = pos05_X; pos_Y = pos05_Y; XY_coor = XY_5
    elif i == 5:
        pos_X = pos06_X; pos_Y = pos06_Y; XY_coor = XY_6
    elif i == 6:
        pos_X = pos07_X; pos_Y = pos07_Y; XY_coor = XY_7
    elif i == 7:
        pos_X = pos08_X; pos_Y = pos08_Y; XY_coor = XY_8
    else:
        pos_X = pos09_X; pos_Y = pos09_Y; XY_coor = XY_9

    # read the RGB image obtained by camera in gray: flag = 0
    img = cv2.imread(image_path, 0)
    # crop the ROI near the laser spot: a temporary centroid (pos_X, pos_Y)
    img_cropped = def_Img_crop(img, pos_X, pos_Y)
    # image processing: (0 ~ 255) to (100 ~ 255) in gray scale
    img_threshold = def_Gray_threshold(img_cropped, threshold)
    # find a centroid of the threshold gray image
    centroid, x_cent, y_cent, num_x, num_y = def_Img_centroid(img_threshold)

    # calculate the thickness using the calibration equation
    if i == 0: C1 = 2771285.27; C2 = -1.369200512; C3 = 1092.024643; C4 = -0.001005219
    elif i == 1: C1 = 1349999.959; C2 = -1.388791884; C3 = 2419.919319; C4 = -0.001330484
    elif i == 2: C1 = 507281.4577; C2 = -1.075253403; C3 = 1080.377993; C4 = -0.001413933
    elif i == 3: C1 = 1449998.92; C2 = -1.46782057; C3 = 2685.134518; C4 = -0.001425463
    elif i == 4: C1 = 3000178.573; C2 = -1.212854051; C3 = 150867.1463; C4 = -0.015492681
    elif i == 5: C1 = 1027000.03; C2 = -1.246059782; C3 = 1910.637241; C4 = -0.0012678
    elif i == 6: C1 = 730769.3074; C2 = -1.060069619; C3 = 465.9036471; C4 = -0.002442971
    elif i == 7: C1 = 919717.9; C2 = -1.283330639; C3 = 2127.108316; C4 = -0.00138829
    else: C1 = 538237.0382; C2 = -1.104531316; C3 = 1344.237117; C4 = -0.001393184
    thickness = def_curvefitting(num_x, C1, C2, C3, C4)
    data_thickness.append(thickness)

  return data_thickness


def decide_pass_fail(thicknesses:list[float]) -> list[str]:
  return ['1' if v < PASS_FAIL_THRESHOLD[i] else '0' for i, v in enumerate(thicknesses)]
   

def def_Img_crop(img, X, Y):
  img_cropped = img[Y - crop_size_half : Y + crop_size_half, X - crop_size_half : X + crop_size_half]
  return img_cropped

def def_Gray_threshold(img, threshold):
  img_Gray_threshold = np.where(img > threshold, 255, 0)
  return img_Gray_threshold

def def_Img_centroid(img_threshold):
  height, width = img_threshold.shape[:2]
  x = []; y = []
  for i in range(height):  # row, y
    for j in range(width):  # column, x
      if img_threshold[i][j] == 255:
        x.append(j)
        y.append(i)
  x_cent = sum(x)/len(x)      # len(x) = len(y) = Area
  y_cent = sum(y)/len(y)
  centroid = (x_cent, y_cent)
  return centroid, x_cent, y_cent, len(x), len(y)

def def_curvefitting(intensity, C1, C2, C3, C4):
    thickness = (C1 * intensity ** C2 + C3 * math.exp(C4 * intensity)) / 2
    return thickness


def main():
  parser = argparse.ArgumentParser(description="Estimate Innercase thicknesses")
  parser.add_argument('image', metavar='image-file-path', help='target image file path')
  parser.add_argument('--output', metavar='thickness-values')

  args = parser.parse_args()

  thicknesses = estimate_thickness(args.image)
  pass_fails = decide_pass_fail(thicknesses)
  pass_fails_str = ','.join(pass_fails)

  print(f"Thicknesses: {pass_fails_str}")
  with open(args.output, "w") as file:
    file.write(f'"{pass_fails_str}"')

if __name__ == '__main__':
    main()