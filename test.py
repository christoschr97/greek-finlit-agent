# THIS FILE IS NOTHING IN THE PROJECT
# THIS FILE IS JUST TO UNDERSTAND STUFF
import streamlit as st
import random

import streamlit as st

st.title("Simple Increment Counter")

print('rerun')
count = 0
print('before if')
print(count)
def increment_counter():
    count += 1
print('after if')
print(count)
slider_value = st.slider("Select a value", 0, 100, 50)
count = 50