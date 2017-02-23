import time

import numpy as np

M = 1  # Mushroom
T = 2  # Tomato

R = 0  # number of rows
C = 0  # number of columns
L = 0  # minimum number of each ingredient per slice
H = 0  # maximum total number of cells of a slice


def read_file(filename):
    # write into global variables
    global R, C, L, H
    # open file
    with open(filename, 'r') as f:
        # read first line with general information
        header = f.readline()
    # remove linebreak '\n' and split numbers
    header = header.rstrip('\n').split(' ')
    # convert strings into int
    header_list = map(int, header)
    # save in global variable
    [R, C, L, H] = header_list

    # Choose data type of numpy array to be a String with length C
    dtype = np.dtype('S{}'.format(C))
    # Load file and skip first line with the header info
    pizza_line_string = np.loadtxt(filename, skiprows=1, dtype=dtype)

    # Parse rows into matrix format
    # Create a new array with shape R rows and C columns of single character data type
    pizza_matrix_string = np.empty((R, C), 'S1')
    for idx, row in enumerate(pizza_line_string):
        pizza_matrix_string[idx] = list(row)

    global M, T
    # Create empty new matrix with shape of pizza_matrix_string
    pizza_matrix_numbers = np.empty(pizza_matrix_string.shape, dtype=int)
    # Set value of T everywhere pizza_matrix_string is equal to 'T'
    pizza_matrix_numbers[np.where(pizza_matrix_string == 'T')] = T
    pizza_matrix_numbers[np.where(pizza_matrix_string == 'M')] = M

    return pizza_matrix_numbers


filename = "medium.in"
# stefan's test
a = 1
for i in range(1,10):
    a+=i
    # my comment

start_time = time.time()
pizza_matrix = read_file(filename)
print("Reading took {} seconds".format(time.time() - start_time))

print(pizza_matrix)
print(R, C, L, H)
