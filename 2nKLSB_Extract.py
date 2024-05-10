import sys
import cv2
import numpy as np
import math


def decode_data(stego_path, bits):
    F = '@'  # initiate the delimiter
    replacedBits = bits  # initiate number of least significant bits to embed
    B = math.ceil(8 / replacedBits)  # Calculate the number of Bytes required for one byte of data
    mask = (1 << replacedBits) - 1
    meta = ''
    secret_msg = ''
    stego_img = cv2.imread(stego_path, cv2.IMREAD_ANYCOLOR)
    shape = stego_img.shape
    stego_pixels_1d = np.reshape(stego_img, -1)
    size = calculate_size(shape)
    i = 0
    while i < size // B:
        cur_data = (stego_pixels_1d[i * B: (i + 1) * B])
        pixel_val = 0
        for index in range(len(cur_data)):
            pixel_val = pixel_val | (cur_data[index] & mask) << (index * replacedBits)

        ch = chr(pixel_val)
        i = i + 1
        if ch == F:
            break
        meta = meta + ch
    msg_length = int(meta) + i
    assert msg_length <= check_capacity(shape, replacedBits), "Stego image is not correct or corrupted"
    while i < msg_length:
        secret_msg_idx = (stego_pixels_1d[i * B: (i + 1) * B])
        pixel = 0
        for index in range(len(secret_msg_idx)):
            pixel = pixel | (secret_msg_idx[index] & mask) << (index * replacedBits)
        ch = chr(pixel)
        secret_msg = secret_msg + ch
        i = i + 1
    return secret_msg


def check_capacity(img_shape, bits):
    if len(img_shape) == 3:
        capacity = (img_shape[0] * img_shape[1] * 3) // bits
        return capacity

    else:
        capacity = img_shape[0] * img_shape[1] // bits
        return capacity


def calculate_size(img_shape):
    if len(img_shape) == 3:
        return img_shape[0] * 3

    else:
        return img_shape[0]


def write_secret_msg(s_msg):
    f = open("./Dataset/RGB/secret.txt", "x")
    f.write(s_msg)
    f.close()


if __name__ == '__main__':

    if len(sys.argv) == 3:
        img_path = sys.argv[1]
        msg = decode_data(img_path, int(sys.argv[2]))
        write_secret_msg(msg)
        print("=============================================================")
        print("=============================================================")
        print("Successfully extracted the secret message.")
        print("Successfully saved a secret.txt file with the secret message.")
        print("=============================================================")
        print("=============================================================")
