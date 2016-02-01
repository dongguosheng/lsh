# -*- coding: gbk -*-

'''
Jianqiu Ji, 2012. Super-Bit Locality-Sensitive Hashing.
'''

from rhplsh import RHPLSH
import numpy as np

class SPBLSH(RHPLSH):
    def init_hyperplane(self):
        self.planes = np.array([])
        for i in range(self.n_table):
            tmp = np.random.randn(self.n_dim, self.n_bit)
            Q, _ = np.linalg.qr(tmp)
            self.planes = np.append(self.planes, Q.T)
        self.planes = self.planes.reshape(self.n_table, self.n_bit, self.n_dim)
