# -*- coding: gbk -*-

import numpy as np
from lsh import LSH
from bitarray import bitarray
from operator import itemgetter

class Index(object):
    def __init__(self, lsh, docinfo_lsh=None):
        self.lsh = lsh
        self.index_dict = {}
        self.docinfo_list = []
        self.docid_list = []
        self.docinfo_lsh = docinfo_lsh
        self.doc_num = 0

    def index(self, input_list, docid):
        key_list = self.lsh.hash(input_list)
        for i, key in enumerate(key_list):
            key += ('_' + str(i))
            self.index_dict.setdefault( key, set() )
            self.index_dict[key].add(self.doc_num)
        docinfo = ''
        if self.docinfo_lsh is None:
            docinfo = np.array(input_list, dtype='float32')
        else:
            docinfo = ''.join(self.docinfo_lsh.hash(input_list))
        self.docinfo_list.append(docinfo)
        self.docid_list.append(docid)
        self.doc_num += 1

    def query(self, input_list, topk=10, key_dist=1, dist_func=LSH.cosine_dist):
        query_docinfo = ''
        if self.docinfo_lsh is None:
            query_docinfo = np.array(input_list, dtype='float32')
        else:
            query_docinfo = bitarray(''.join(self.docinfo_lsh.hash(input_list)))
            
        rs_dict = {}
        if key_dist >= 0:
            query_key_list = self.lsh.hash(input_list)
            for i, query_key in enumerate(query_key_list):
                for k in LSH.get_keys_str(query_key, key_dist):
                    k += ('_' + str(i))
                    if k in self.index_dict:
                        for idx in self.index_dict[k]:
                            if idx in rs_dict:
                                continue
                            dist = dist_func(self.docinfo_list[idx], query_docinfo)
                            docid = self.docid_list[idx]
                            rs_dict[docid] = dist
        else:
            # brute force search
            for docid, docinfo in zip(self.docid_list, self.docinfo_list):
                dist = dist_func(docinfo, query_docinfo)
                rs_dict[docid] = dist
        print 'Candidates: %d' % len(rs_dict)
        return (sorted(rs_dict.items(), key=itemgetter(1), reverse=False)[: topk], len(rs_dict))

    def save(self, output):
        # save index to text file
        with open(output + '.index', 'w') as fout:
            for k, v in self.index_dict.items():
                fout.write(k + ',')
                for idx in v:
                    fout.write('%d ' % idx)
                fout.write('\n')
        # save docid and docinfo
        np.save(output + '.docinfo', self.docinfo_list)
        np.save(output + '.docid', np.array(self.docid_list, dtype='uint64'))
        self.lsh.save(output + '_index')
        if self.docinfo_lsh is not None:
            self.docinfo_lsh.save(output + '_docinfo')

    def load(self, input):
        # load index from text file
        with open(input + '.index', 'r') as fin:
            for line in fin:
                key, vals = line.rstrip().split(',')
                self.index_dict[key] = [int(idx) for idx in vals.split()]
        # load docid and docinfo
        self.docinfo_list = []
        docinfo_list = np.load(input + '.docinfo.npy')
        if self.docinfo_lsh is not None:
            for docinfo in docinfo_list:
                self.docinfo_list.append(bitarray(docinfo))
        else:
            self.docinfo_list = docinfo_list
        self.docid_list = np.load(input + '.docid.npy')
        assert len(self.docinfo_list) == self.docid_list.shape[0]
        self.doc_num = self.docid_list.shape[0]
        # load lsh
        self.lsh.load(input + '_index')
        if self.docinfo_lsh is not None:
            self.docinfo_lsh.load(input + '_docinfo')
        print self

    def __str__(self):
        return 'index bit num: %d, index dict size: %d, doc_num: %d' % (self.lsh.n_bit, len(self.index_dict), self.doc_num)

