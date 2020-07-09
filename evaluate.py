#!/usr/bin/env python
import sys, os, os.path
import numpy as np
import json
from sklearn.metrics import roc_auc_score

def dcg_score(y_true, y_score, k=10):
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    gains = 2 ** y_true - 1
    discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gains / discounts)


def ndcg_score(y_true, y_score, k=10):
    best = dcg_score(y_true, y_true, k)
    actual = dcg_score(y_true, y_score, k)
    return actual / best


def mrr_score(y_true, y_score):
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order)
    rr_score = y_true / (np.arange(len(y_true)) + 1)
    return np.sum(rr_score) / np.sum(y_true)

def scoring(truth_f, sub_f):
    aucs = []
    mrrs = []
    ndcg5s = []
    ndcg10s = []
    
    line_index = 1
    for lt in truth_f:
        ls = sub_f.readline()
        
        # json deserialize
        lt = json.loads(lt)
        
        # ignore masked lines
        if lt['impression'] == []:
            continue
        
        try:
            ls = json.loads(ls)
        except:
            # print("Line-{} can not be deserialized by json. Filled with 0 ranks".format(line_index))
            ls = {'uid': lt['uid'], 
                  'time': lt['time'],
                  'impression': {k: 0 for k in lt['impression']}}   
        
        # check UID and time
        if lt['uid'] != ls['uid'] or lt['time'] != ls['time']:
            raise ValueError("Line-{} submission uid and time do not match. Expect {} and {}, but get {} and {}".format(
                line_index,
                lt['uid'],
                lt['time'],
                ls['uid'],
                ls['time']
            ))
            
        y_true = []
        y_score = []

        ltsess = lt['impression']
        lssess = ls['impression']
        
        lt_len = float(len(ltsess))
        for k, v in ltsess.items():
            y_true.append(v)
            score_rslt = 1 - lssess[k]/lt_len
            if score_rslt < 0 or score_rslt > 1:
                raise ValueError("Line-{}: score_rslt should be int from 0 to {}".format(
                    line_index,
                    lt_len
                ))
            y_score.append(score_rslt)
        
        auc = roc_auc_score(y_true,y_score)
        mrr = mrr_score(y_true,y_score)
        ndcg5 = ndcg_score(y_true,y_score,5)
        ndcg10 = ndcg_score(y_true,y_score,10)
        
        aucs.append(auc)
        mrrs.append(mrr)
        ndcg5s.append(ndcg5)
        ndcg10s.append(ndcg10)
        
        line_index += 1

    return np.mean(aucs), np.mean(mrrs), np.mean(ndcg5s), np.mean(ndcg10s)
        

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    submit_dir = os.path.join(input_dir, 'res') 
    truth_dir = os.path.join(input_dir, 'ref')


    if not os.path.isdir(submit_dir):
        print("%s doesn't exist" % submit_dir)

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, 'scores.txt')              
        output_file = open(output_filename, 'wb')

        truth_file = open(os.path.join(truth_dir, "truth.json"), 'r')
        submission_answer_file = open(os.path.join(submit_dir, "prediction.json"), 'r')
        
        auc, mrr, ndcg, ndcg10 = scoring(truth_file, submission_answer_file)

        output_file.write("AUC:{:.4f}\nMRR:{:.4f}\nnDCG@5:{:.4f}\nnDCG@10:{:.4f}".format(auc, mrr, ndcg, ndcg10))
        output_file.close()