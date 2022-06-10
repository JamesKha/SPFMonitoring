import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['API_KEY']

st.title(body='SPF Monitor')
st.header(body='SPF Monitor')

city_name = st.text_input(label='Enter city:')
submit_btn = st.button(label='Submit')
if(submit_btn):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'
    res = requests.request(method='GET', url=url)
    st.write(res.content)
