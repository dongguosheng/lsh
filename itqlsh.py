# -*- coding: gbk -*-

'''
LSH Based on Iterative Quantization.
Y. Gong and S. Lazebnik. 2011. Iterative Quantization: A Procrustean Approach to Learning Binary Codes.
Yeqing Li, Chen Chen. 2014. Sub-Selective Quantization for Large-Scale Image Search.
'''

import numpy as np
from numpy import linalg as la
from operator import itemgetter
from lsh import LSH
import sys

class ITQLSH(LSH):
    def __init__(self, n_bit, n_dim, n_table=5, sample_rate=0.025, n_iter=50):
        self.n_bit = n_bit
        self.n_dim = n_dim
        self.n_table = n_table
        self.sample_rate = sample_rate
        self.n_iter = n_iter
        self.pca_list = []
        self.R_list = []

    def pca(self, sample_arr):
        '''
        Do PCA on samples of array.
        '''
        if not isinstance(sample_arr, np.ndarray):
            raise Exception("sample_arr type is %s, arr must be numpy.ndarray." % str(type(sample_arr)))
        sample_arr -= sample_arr.mean(axis=0)
        cov_arr = np.cov(sample_arr, rowvar=0)
        eig_val, eig_vec = la.eigh(cov_arr)
        idx = np.argsort(eig_val)[:: -1]
        pca_arr = eig_vec[:, idx][:, : self.n_bit]
        self.pca_list.append(pca_arr)

    def train(self, arr):
        '''
        Train PCA and R.
        '''
        if not isinstance(arr, np.ndarray):
            raise Exception("arr type is %s, arr must be numpy.ndarray." % str(type(arr)))
        n_sample = int(arr.shape[0] * self.sample_rate)
        print 'Sample Num: %d' % n_sample
        for i in range(self.n_table):
            index = np.random.choice(arr.shape[0], n_sample, replace=False)
            sample_arr = arr[index, :]
            self.pca(arr)
            R = np.random.normal(self.n_bit, self.n_bit)
            V = np.dot(sample_arr, self.pca_list[-1])
            for j in range(self.n_iter):
                print_str = '%d(%d), table %d\r' % (j+1, self.n_iter, i+1)
                sys.stdout.write(print_str)
                sys.stdout.flush()
                B = np.sign(np.dot(V, R))
                U, _, V = la.svd(np.dot(B.T, V))
                R = np.dot(V.T, U.T)    # transpose V or not?
            self.R_list.append(R)
        print '\ntrain complete.'

    def hash(self, input_list):
        '''
        Hash input_list to n_bit of binarys.
        '''
        bits_list = []
        for pca_arr, R in zip(self.pca_list, self.R_list):
            B = np.dot(np.dot(np.array(input_list), pca_arr), R)
            key = ''.join(['1' if e > 0 else '0' for e in B])
            bits_list.append(key)
        return bits_list

    def dist(self, input_list1, input_list2):
        bits_list1 = self.hash(input_list1)
        bits_list2 = self.hash(input_list2)
        return sum([self.hamming_dist_str(bits_arr1, bits_arr2) for bits_arr1, bits_arr2 in zip(bits_list1, bits_list2)]) / float(self.n_table)

    def save(self, output):
        '''
        Save PCA-ITQ params.
        '''
        np.save(output + '.pca', self.pca_list)
        np.save(output + '.R', self.R_list)
        print 'save complete.'

    def load(self, input):
        '''
        '''
        self.pca_list = np.load(input + '.pca.npy')
        self.R_list = np.load(input + '.R.npy')
        assert self.pca_list.shape[0] == self.R_list.shape[0]
        self.n_bit = self.R_list.shape[2]
        self.n_dim = self.pca_list.shape[1]
        self.n_table = self.pca_list.shape[0]
        print self
        print 'load complete.'

    def load_txt(self, input):
        '''
        Load From Txt File.
        '''
        with open(input) as fin:
            head = fin.next()
            self.n_bit, self.n_dim, self.n_table, self.sample_rate, self.n_iter = head.rstrip().split()
            self.n_bit = int(self.n_bit)
            self.n_dim = int(self.n_dim)
            self.n_table = int(self.n_table)
            self.sample_rate = float(self.sample_rate)
            self.n_iter = int(self.n_iter)
            # load pca mat
            n_row = 0
            tmp_list = []
            while n_row < self.n_dim * self.n_table:
                line = fin.next()
                tmp_list.extend([float(e) for e in line.rstrip().split()])
                n_row += 1
            self.pca_list = np.array(tmp_list).reshape(self.n_table, self.n_dim, self.n_bit)
            # load r mat
            n_row = 0
            tmp_list = []
            while n_row < self.n_bit * self.n_table:
                line = fin.next()
                tmp_list.extend([float(e) for e in line.rstrip().split()])
                n_row += 1
            self.R_list = np.array(tmp_list).reshape(self.n_table, self.n_bit, self.n_bit)
            print self
            print 'load txt model complete.'

    def __str__(self):
        return 'n_bit: %d, n_dim: %d, n_table: %d, sample_rate: %f, n_iter: %d' % (self.n_bit, self.n_dim, self.n_table, self.sample_rate, self.n_iter)
