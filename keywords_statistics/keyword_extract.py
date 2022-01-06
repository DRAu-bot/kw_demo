from jieba import analyse
from .ac_machine import AcMachine

with open(r'keywords_statistics/dict/custom20211216.dic', 'r',encoding="utf-8") as f:
    dict_tezign=[i.replace("\n","") for i in f.readlines()]
def ac_machine_extract(text,dict_tezign):#基于词典匹配的关键词提取，选用ac自动机算法（最速算法）
    ac_machine=AcMachine(dict_tezign)
    info=ac_machine.map_actree(text)
    info=list(set([i["word"] for i in info]))
    return info

def tfidf_extract_kw(text):#基于tfidf（一种关键词提取算法）的关键词提取
    kw_tfidf = analyse.extract_tags(text, withWeight=True, allowPOS=(), withFlag=False)
    return [i[0] for i in kw_tfidf]


def kws_extract(text):#主要提取关键词功能，输入一个string，输出一个关键词list。融合上述两种算法
    text_list=list()
    text_list.extend(tfidf_extract_kw(text))
    text_list.extend(ac_machine_extract(text,dict_tezign))
    text_list=list(set(text_list))
    return text_list

