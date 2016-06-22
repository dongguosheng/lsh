# -*- coding: gbk -*-

'''
LSH Based on Random Hyperplane Projection.
Charikar, M. S. 2002. Similarity estimation techniques from rounding algorithms.
'''

import numpy as np
from lsh import LSH
from bitarray import bitarray

class RHPLSH(LSH):
    def __init__(self, n_bit, n_dim, n_table=5):
        self.n_dim = n_dim
        self.n_bit = n_bit
        self.n_table = n_table
        self.planes = ''

    def init_hyperplane(self):
        self.planes = np.array([])
        for i in range(self.n_table):
            self.planes = np.append(self.planes, np.random.randn(self.n_bit, self.n_dim))
        self.planes = self.planes.reshape(self.n_table, self.n_bit, self.n_dim)

    def hash(self, input_list):
        bits_list = []
        for plane in self.planes:
            projection = np.dot(plane, np.array(input_list))
            bits_list.append(''.join(['1' if e > 0 else '0' for e in projection]))
        return bits_list

    def dist(self, input_list1, input_list2):
        bits_list1 = self.hash(input_list1)
        bits_list2 = self.hash(input_list2)
        return sum([self.hamming_dist_str(bits_arr1, bits_arr2) for bits_arr1, bits_arr2 in zip(bits_list1, bits_list2)]) / float(self.n_table)

    def save(self, output):
        '''
        Save params.
        '''
        np.save(output + '.planes', self.planes)

    def load(self, input, docinfo_ext=True):
        '''
        Load params, hyperplanes, index, docinfo.
        '''
        self.planes = np.load(input + '.planes.npy')
        self.n_table, self.n_bit, self.n_dim = self.planes.shape

    def __str__(self):
        return 'n_bit: %d, n_dim: %d, n_table: %d' % (self.n_bit, self.n_dim, self.n_table)
