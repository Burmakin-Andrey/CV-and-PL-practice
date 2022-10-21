from numpy.ma.core import zeros_like
from skimage.measure import label
import numpy as np
from scipy.ndimage.morphology import binary_opening


def neighbors_count(arr, y, x):
  return int(arr[y-1][x]>0) + int(arr[y+1][x]>0) + int(arr[y][x-1]>0) + int(arr[y][x+1]>0)


def fig_size(arr, y, x):
  xe = x
  ye = y

  while neighbors_count(arr,y,xe) > 0:  
    xe += 1
  while neighbors_count(arr,ye,x) > 0:  
    ye += 1
  return ye-1, xe-1 

image = np.load("ps.npy")
struct = np.zeros((3,1))
image2 = label(image)
arr = []
id = 0
start = 0
stop = 0

masks = []
for y in range(image2.shape[0]):
  for x in range(image2.shape[1]):


    if image2[y][x] > id:
      ye, xe = fig_size(image, y, x)
      mask = image[y:ye, x:xe].tolist()
      
      if ([mask] not in masks):
        masks.append([mask])

      id += 1

countArr = []

for mask in masks:
  maskedImg = binary_opening(image, np.array(mask[0]))
  labeled = label(maskedImg)
  image -=maskedImg
  countArr.append(labeled.max())



count = 0
for i in masks:
  print("For figure:")
  print(np.array(i[0]))
  print(f"Found {countArr[count]} matches.")
  count+=1



