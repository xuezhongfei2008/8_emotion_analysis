# -*- coding: utf-8 -*-

import numpy as np  # 导入numpy
import pandas as pd
import jieba

jieba.load_userdict("/opt/gongxf/python3_pj/Robot/original_data/finWordDict.txt")
stop_words_path = '/opt/gongxf/python3_pj/Robot/original_data/stop_words.txt'


def stop_words():
    stopwords = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
    return stopwords


stopword = stop_words()


def load_dict():
    # 开始加载情感词典
    negdict = []  # 消极情感词典
    posdict = []  # 积极情感词典
    nodict = []  # 否定词词典
    plusdict = []  # 程度副词词典
    sl = pd.read_csv('dict/neg.txt', header=None, encoding='utf-8')
    for i in range(len(sl[0])):
        negdict.append(sl[0][i])
    sl = pd.read_csv('dict/pos.txt', header=None, encoding='utf-8')
    for i in range(len(sl[0])):
        posdict.append(sl[0][i])
    sl = pd.read_csv('dict/no.txt', header=None, encoding='utf-8')
    for i in range(len(sl[0])):
        nodict.append(sl[0][i])
    sl = pd.read_csv('dict/plus.txt', header=None, encoding='utf-8')
    for i in range(len(sl[0])):
        plusdict.append(sl[0][i])
    return negdict, posdict, nodict, plusdict


# 基于字典计算情感值
def predict(s, negdict, posdict, nodict, plusdict):
    p = 0
    sd = list(jieba.cut(s))
    # print("sd_cut",sd_cut)
    # sd=([word for word in sd_cut if word not in stopword])
    print("sd", sd)
    for i in range(len(sd)):
        if sd[i] in negdict:
            if i > 0 and sd[i - 1] in nodict:
                p = p + 1
            elif i > 0 and sd[i - 1] in plusdict:
                p = p - 2
            else:
                p = p - 1
        elif sd[i] in posdict:
            if i > 0 and sd[i - 1] in nodict:
                p = p - 1
            elif i > 0 and sd[i - 1] in plusdict:
                p = p + 2
            elif i > 0 and sd[i - 1] in negdict:
                p = p - 1
            elif i < len(sd) - 1 and sd[i + 1] in negdict:
                p = p - 1
            else:
                p = p + 1
        elif sd[i] in nodict:
            p = p - 0
    return p


def test():
    negdict, posdict, nodict, plusdict = load_dict()
    df = pd.read_excel("../data/data_0718.xlsx")
    for ii in range(len(df)):
        s = df['question'][ii]
        prob = predict(s, negdict, posdict, nodict, plusdict)
        print("prob", prob)


if __name__ == '__main__':
    test()
    # negdict, posdict, nodict, plusdict = load_dict()
    # while True:
    #     s = input("请输入测试问题：")
    #     prob = predict(s, negdict, posdict, nodict, plusdict)
    #     print("prob", prob)
