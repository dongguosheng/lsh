# -*- coding: gbk -*-

'''
Weihao Kong, Wu-Jun Li, 2012. Double-Bit Quantization for Hashing.
'''

import numpy as np

class DBQ(object):
    def __init__(self):
        self.thresholds_list = []

    def gen_thresholds(self, proj_mat_list):
        '''
        Make sure input proj_mat_list(n_table, n_bit, n_point) is subjected to Gaussian distribution.
        '''
        cnt = 0
        for proj_mat in proj_mat_list:
            for col in proj_mat:
                s1 = []
                s2 = []
                s3 = []
                for e in col:
                    if e > 0:
                        s3.append(e)
                    else:
                        s1.append(e)
                s1.sort(reverse=True)
                s3.sort()
                f_max = 0
                i = 0
                j = 0
                sum1 = sum(s1)
                n_s1 = len(s1)
                sum2 = 0
                sum3 = sum(s3)
                n_s3 = len(s3)
                left = 0
                right = 0
                s1_max = -100
                s2_max = -100
                while(i < len(s1) or j < len(s3)):
                    if sum2 <= 0 and j < len(s3):
                        s2.append(s3[j])
                        sum2 += s3[j]
                        sum3 -= s3[j]
                        s2_max = s3[j]
                        j += 1
                        n_s3 -= 1
                    elif sum2 > 0 and i < len(s1):
                        s2.append(s1[i])
                        sum2 += s1[i]
                        sum1 -= s1[i]
                        i += 1
                        n_s1 -= 1
                        if i < len(s1):
                            s1_max = s1[i]
                    else:
                        pass
                    part1 = part2 = 0
                    if n_s1 > 0:
                        part1 = sum1 ** 2 / n_s1
                    if n_s3 > 0:
                        part2 = sum3 ** 2 / n_s3
                    f = part1 + part2
                    if f > f_max:
                        left = s1_max
                        right = s2_max
                        f_max = f
                        # print 'left: %f, right: %f, f_max: %f' % (left, right, f_max)
                # print 'final => left: %f, right: %f, f_max: %f' % (left, right, f_max)
                self.thresholds_list.extend( (left, right) )
            cnt += 1
            print 'tabel %d complete.' % cnt
        self.thresholds_list = np.array(self.thresholds_list).reshape(proj_mat_list.shape[0], 2, proj_mat_list.shape[1])

    def quantization(self, proj_arr, thresholds):
        '''
        proj_arr: (n_bit, )
        thresholds: (n_bit, 2)
        '''
        assert proj_arr.shape[0] == thresholds.shape[0]
        bit_str = ''
        for val, left_right in zip(proj_arr, thresholds):
            left, right = left_right
            if val <= left:
                bit_str += '01'
            elif val > left and val <= right:
                bit_str += '00'
            else:
                bit_str += '10'
        return bit_str
