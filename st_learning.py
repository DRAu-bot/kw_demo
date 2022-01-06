import streamlit as st
import sys
sys.path.append("../")

from keywords_statistics import kws_extract
import re

def clean_kws(kws):
    kws_out=list()
    for kw in kws:
        judge_str = re.search(r"\W*",kw)
        if judge_str:
            kw=re.sub(r"\W*","",kw)
            
            if kw=="":
                continue
        kws_out.append(kw)
    return kws_out

def make_text_label(text):
    kws=kws_extract(text)
    kws=clean_kws(kws)
    module=kws[0]
    for kw in kws[1:]:
        module+="|"+kw
    text_out=re.sub(module,r"【\g<0>】",text)
    return text_out,kws

st.text("\n"*10)
st.title("关键词抽取Demo")

text = st.text_input('文本')
if text !="":
    text_label=make_text_label(text)[0]
    st.write('关键词文本为')
    st.write(text_label)
