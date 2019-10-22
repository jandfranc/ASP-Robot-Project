import numpy as np
from skimage.io import imread
from PIL import Image

def map_read_skimage(map):
    map_arr = imread(map)
    result = map_arr[:, :, 0]
    for i_height in range(0,result.shape[0]):
        for i_width in range(0,result.shape[1]):
            if result[i_height][i_width] < 100:
                result[i_height][i_width] = 0
            elif result[i_height][i_width] >225:
                result [i_height][i_width] = 1
            else:
                result[i_height][i_width] = 2
    return result

def map_read(map):
    map_arr = np.asarray(Image.open('map.jpeg'))
    result = np.copy(map_arr[:, :, 0])
    for i_height in range(0,result.shape[0]):
        for i_width in range(0,result.shape[1]):
            if result[i_height][i_width] < 100:
                result[i_height][i_width] = 0
            elif result[i_height][i_width] >225:
                result [i_height][i_width] = 1
            else:
                result[i_height][i_width] = 2
    return result
