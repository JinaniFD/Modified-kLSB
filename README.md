# Modified-kLSB

Algorithm A - 2nKLSB_Encode.py
Algorithm B - 2nKLSB_Encode.py

This has two python files that perform data hiding and extracting using a modified kLSB technique.
The 2nKLSB_Encode.py requires 3 command line arguments.
First argument is the cover image, second is the .txt file that contain the secret message and
the third argument is the number of bits to use to hide data. This can be 2, 3 or 4.
An an output a *_stego_Demo.* file will be created.
This accepts .tiff, .tif, .png, .bmp, .pgm file types.
For example
% python 2nKLSB_Encode.py [cover image .txt] [file with secret message] [3] 

When extracting, 2nKKLSB_Extract.py requires two arguments. First is the cover image and the second is the number of
bits to extract. AS an output this will create a secret.txt file with the extracted message.
If 3 bits were used to encode same number of bits must be given as the argument.
For example
% python 2nKLSB_Encode.py [stego image] [3]
