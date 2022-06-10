from pyrsistent import s
import streamlit as st
import pandas as pd
import numpy as np
import requests as re
import json
import pgeocode




def determineSkinType(): 
    st.title('determine ')
    with st.form("skin_type"):
        skin = st.selectbox(
        'Select skin color',
        ("very light", "light", "light brown", "olive-colored", "dark brown", "black"))
        hair  = st.selectbox(
        'Select hair color',
        ("blond","dark blond",  "brown", "dark brown", "black" ))
        eyeColor =  st.selectbox(
        'Select eye color',
        ("blue","gray",  "brown", "dark brown" ))
        submitted = st.form_submit_button("Submit")

        if skin == "very light":
            type = "I"
        if skin == "light": 
            if hair == "blond":
                type = "II"
            else: 
                type = "II or III"
        elif skin == "light brown":
            if hair == "dark blond" or hair == "brown":
                type = "III"
            else:
                type = "IV"
        elif skin == "olive":
            type = "IV"
        elif skin == "dark brown": 
            if hair == "dark brown" or hair == "black": 
                type = "V or VI"
        else:
            type = "VI"
        
            
            
        if submitted:
            st.write("Skin Type:", type)

        

def mainPage():
    st.title('Main Page')
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

page_names_to_funcs = {
    "Main Page": mainPage,
    "Skin Type Test": determineSkinType,
    
}

demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()