# lsh
locality-sensitive hashing index, learning to hash.
an alternative to index large scale high dimensional data.

# Index gensim Word2Vec model using rhplsh

    import numpy as np
    from gensim import models
    from lsh.rhplsh import RHPLSH
    from lsh.itqlsh import ITQLSH
    from lsh.lsh import LSH
    from lsh.index import Index
    
    w2v = models.Word2Vec.load('./w2v_model/word2vec.model')
    n_bit = 20
    n_dim = 200
    n_table = 5
    rhplsh = RHPLSH(n_bit, n_dim, n_table=n_table)
    rhplsh.init_hyperplane()
    w2v_index = Index(rhplsh)
    now = datetime.now()
    idx = 0
    for v in w2v.syn0:
        w2v_index.index(v, idx)
        idx += 1
    print '\nINDEX COST: ' + str(datetime.now() - now)
    w2v_index.save('w2v')   # Four files will be generated: `w2v.index`, `w2v.docinfo`, `w2v.docid`, `w2v.planes`
    w2v_index.load('w2v')
    w = 'word'
    rs_list, recall_num = w2v_index.query(w2v[w], topk=30, key_dist=1, dist_func=LSH.cosine_dist)
    print 'query: %s' % w
    print 'recall num: %d' % recall_num
    for word_id, dist in rs_list:
        print w2v.index2word[word_id], dist

