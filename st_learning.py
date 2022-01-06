import streamlit as st
import sys
sys.path.append("../")

from keywords_statistics import kws_extract
import re
def make_text_label(text):
    kws=kws_extract(text)
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