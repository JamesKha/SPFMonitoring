from pyrsistent import s
import streamlit as st
import pandas as pd
import numpy as np
import requests as re
import json
import pgeocode
import time

st.title('Testing')

with st.form("my_form"):
    country = st.selectbox(
    'Select Country Code',
    ('us', 'ca'))

    zip_code =  st.text_input(label="ZIP/Postal Code",  disabled=False)


    nomi = pgeocode.Nominatim(country)
    nomi_respository = nomi.query_postal_code(zip_code)

    lat, long = nomi_respository['latitude'],nomi_respository['longitude']


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

    submitted = st.form_submit_button("Submit")

    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid=bae1369f17f11704a9f3fc181dbba78c".format(lat, long)
    payload={}
    headers = {}
    response = re.request("GET", url, headers=headers, data=payload)

    if submitted:
        st.write("Skin Type:", option)
        st.write("You may stay outside for {} minutes".format(duration))
        st.write("Lat:", lat, "Long:", long)
        data = pd.json_normalize(json.loads(response.text))
        st.write("Current UVI", data['current.uvi'][0])

        timer = st.empty()
        if isinstance(duration, int):
            secs = duration * 60
            for exposureTime in range(secs, -1, -1):
                formatTime = time.strftime("%M:%S", time.gmtime(exposureTime))
                timer.metric("UV Exposure Timer", formatTime)
                time.sleep(1)
            st.warning("Timer has expired!")
