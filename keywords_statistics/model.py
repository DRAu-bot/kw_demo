import sys
import pandas as pd 
import json
import numpy as np
import spacy as sp
from spacy.symbols import NOUN,VERB
from collections import defaultdict
from tqdm import tqdm
from jieba import analyse
from keyword_extract import kws_extract

class kw_sta_1D():
    def __init__(self,df,text_col,content_row=""columns_list=[],calculate_dict=dict()):
        self.df=df#入参的excel文件
        self.text_col=text_col#需要统计的文本列
        self.columns_list=columns_list#需要统计计算的效果指标列
        self.calculate_dict=calculate_dict#需要计算的公式列及其公式
        #下为默认执行的代码
        self.id_data=self._get_id_data(self.df,self.text_col,self.content_row,self.columns_list,self.calculate_dict)
        self.kw_data1D=self._get_kw_data1D(self.id_data,self.columns_list,self.calculate_dict)
        self.kw_data_full1D=self._get_kw_data_full1D(self.id_data,self.content_row,self.columns_list,self.calculate_dict)
        
    def _get_id_data(self,df,text_col,content_row,columns_list,calculate_dict):#将原始数据转化为dict
        titles=df[text_col]
        df.reset_index(drop=True,inplace=True)
        id_data=dict()
        df=df[columns_list].fillna(0)
        for col in columns_list:
            if col not in df.columns:
                raise 'col error'
        for index in tqdm(range(len(titles))):
            
            title=titles[index]
            if pd.isnull(title):
                continue
            id_data[title]={'kw':kws_extract(title)}
            for col in columns_list:
                id_data[title][col]=df[col][index]
                id_data[title][content_row]=df[content_row][index]
            for key,func in calculate_dict.items():
                id_data[title][key]=func(id_data[title])
            
        return id_data
    
    def _get_kw_data1D(self,id_data,columns_list,calculate_dict):#基于分词进行统计，返回一个dict
        kw_data=defaultdict(lambda: defaultdict(np.int64))
        for key,values in id_data.items():
            kws=values['kw']
            for kw in kws:
                for col in columns_list:
                    kw_data[kw][col]+=values[col]
#                 kw_data[kw]['转']+=values['转']
#                 kw_data[kw]['赞']+=values['赞']
#                 kw_data[kw]['粉丝量']+=values['粉']
#                 kw_data[kw]['转评赞']+=values['转']+values['评']+values['赞']
                kw_data[kw]['视频数']+=1
        for key,values in kw_data.items(): 
            for col,func in calculate_dict.items():
                kw_data[key][col]=func(values)
        return  kw_data
    def _filt_data(self,kw_data,num=3):
        data=dict()
        for key,values in kw_data.items():

            if values['视频数']>=num:
                data[key]=values
        return data


    def _get_kw_data_full1D(self,id_data,columns_list,calculate_dict):#基于分词的结果回代回原始文本,返回一个dict
        kw_list=list()
        kws=self._filt_data(self.kw_data1D)
        kw_list=list(kws.keys())
        kw_data=defaultdict(lambda: defaultdict(np.int64))
        
        for kw in kw_list:
            for title,values in id_data.items():
                if kw in title:
                    for col in columns_list:
                        kw_data[kw][col]+=values[col]
                    kw_data[kw]['视频数']+=1
                    kw_data[kw]['出现次数']+=title.count(kw)
        for key,values in kw_data.items():
            for col,func in calculate_dict.items():
                kw_data[key][col]=func(values)
        return  kw_data
    def dict2df1D(self,kw_data):#将计算好的dict返回成一个excel
        df_out=pd.DataFrame(columns=['创意词']+list(self.columns_list)+list(self.calculate_dict.keys())+['视频数']+['出现次数'])
 
        j=0
        for key,values in kw_data.items():
            row=[key]+[values[col] for col in df_out.columns[1:]]
            df_out.loc[j]=row
            j+=1
        return df_out
