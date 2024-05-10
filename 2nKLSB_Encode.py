import os.path
import sys
import math
from os import path
import cv2
import numpy as np
import time


def encode_data(cover_path, message, bits):
    F = '@'  # initiate the delimiter
    replacedBits = bits  # initiate the number of bits to embed
    B = math.ceil(8 / replacedBits)  # Calculate the number of Bytes required for one byte of data
    mask = (1 << replacedBits) - 1
    img = cv2.imread(cover_path, cv2.IMREAD_ANYCOLOR)
    ori_shape = img.shape
    print("===========================================")
    print("===========================================")
    print("Original shape of cover : " + str(ori_shape))
    message = '{}{}{}'.format(len(message), F, message)
    if not check_capacity(ori_shape, len(message), replacedBits):
        return "NONE"

    cover_pixels = np.reshape(img, -1)  # Convert the cover image to into 1D array
    for (index, val) in enumerate(message):
        block = cover_pixels[index * B: (index + 1) * B]
        val = ord(val)
        for idx in range(len(block)):
            x = block[idx] % (2 ** replacedBits)  # A mod 2^n
            d = (val >> replacedBits * idx) & mask  # Prepare the data to be inserted
            r = x - d
            if (r > 2**(replacedBits-1)) and (d < 255 - 2**(replacedBits-1)):
                block[idx] = block[idx] - r + 2**replacedBits
            elif (r < -2**(replacedBits-1)) and (x > 2**(replacedBits-1)):
                block[idx] = block[idx] - r - 2**replacedBits
            else:
                block[idx] = block[idx] - r

        cover_pixels[index * B: (index + 1) * B] = block
    return write_stego_image(cover_pixels, ori_shape, cover_path)


def write_stego_image(cover_image, shape, p):
    img = np.reshape(cover_image, shape)
    print("Embedded shape of stego : " + str(img.shape))
    print("===========================================")
    filename = path.splitext(p)
    filename = filename[0] + '_stego_Demo' + filename[1]
    cv2.imwrite(filename, img)
    return filename


def check_capacity(img_shape, length, bits):
    if len(img_shape) == 3:
        capacity = (img_shape[0] * img_shape[1] * 3) // bits
    else:
        capacity = (img_shape[0] * img_shape[1]) // bits

    if length <= capacity:
        return True
    else:
        return False


def read_r_data(r_path):
    file = open(r_path, "r")
    content = file.read()
    # print(content)
    file.close()
    return content


def start(cvr_path, msg, bits):
    s_time = time.time()
    res_path1 = encode_data(cvr_path, msg, bits)
    e_time = time.time()
    elapse = e_time - s_time
    print("Time taken : " + str(elapse) + " seconds")
    print("===========================================")
    print("SECRET DATA SUCCESSFULLY EMBEDDED TO :  " + res_path1 + ".")


if __name__ == '__main__':
    msg_p = ''
    msg1 = ''
    mypath = ''

    if len(sys.argv) == 4:
        mypath = sys.argv[1]  # cover path
        msg_p = sys.argv[2]  # secret mage file path
        msg1 = read_r_data(msg_p)
        start(mypath, msg1, int(sys.argv[3]))
    else:
        mypath = sys.argv[1]
        entered_msg = input(" As you have not provided a secret message file and number of bits, "
                            "Please type your message : ")
        hidden_bits = input(" As you have not provided the number of bits to hide, "
                            "Please type how many bits to use (2/3/4) : ")
        start(mypath, entered_msg,hidden_bits)







