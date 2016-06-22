# -*- coding: gbk -*-

import numpy as np

class LSH(object):
    @staticmethod
    def get_keys(bit_arr, dist):
        bits_list = [bit_arr]
        if dist == 0:
            return bits_list
        for i in range(bit_arr.len):
            tmp_bits = bit_arr
            tmp_bits[i] = not tmp_bits[i]
            bits_list.append(tmp_bits)
        return bits_list

    @staticmethod
    def hamming_dist(bit_arr1, bit_arr2):
        return (bit_arr1^bit_arr2).count(True)

    @staticmethod
    def get_keys_str(bits_str, dist):
        bits_list = [bits_str]
        if dist == 0:
            return bits_list
        for i in range(len(bits_str)):
            tmp_list = list(bits_str)
            if bits_str[i] == '0':
                tmp_list[i] = '1'
            else:
                tmp_list[i] = '0'
            bits_list.append(''.join(tmp_list))
        return bits_list

    @staticmethod
    def hamming_dist_str(bits_str1, bits_str2):
        if len(bits_str1) != len(bits_str2):
            print 'length not equal!'
            return -1
        return sum([0 if i == j else 1 for i, j in zip(bits_str1, bits_str2)])

    @staticmethod
    def cosine_dist(input_arr1, input_arr2):
        return 1.0 - np.dot(input_arr1, input_arr2.T) / np.linalg.norm(input_arr1) / np.linalg.norm(input_arr2)

    @staticmethod
    def euclidean_dist(input_arr1, input_arr2):
        return np.linalg.norm(input_arr1 - input_arr2)
