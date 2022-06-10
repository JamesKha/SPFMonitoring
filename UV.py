import streamlit as st
import pandas as pd
import numpy as np

st.title('Testing')

st.text_input(label="Postal Code",  disabled=False)
option = st.selectbox(
     'Select Skin Type',
     ('I', 'II', 'III', "IV", "V", "VI"))


if option == "I": 
    duration = 10
elif option == "II": 
    duration = 20 
elif option == "III": 
    duration = 30 
elif option == "IV": 
    duration = 50
else:
    duration = "More than 60"

st.write("Skin Type:", option)
st.write("You may stay outside for {} minutes".format(duration))
