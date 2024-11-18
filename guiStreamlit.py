import streamlit as st
import numpy as np

with st.chat_message("assistant"):
    st.write("Hello human") #random message input
    st.bar_chart(np.random.randn(30, 3)) #barchart output

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")