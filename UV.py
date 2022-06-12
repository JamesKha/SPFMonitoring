from pyrsistent import s
from google_images_download import google_images_download as gid
from icrawler.builtin import GoogleImageCrawler
import streamlit as st
import pandas as pd
import numpy as np
import requests as re
import json
import pgeocode
import time

def determineSkinType():
    st.title('Determine Skin Type')
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

def location_image(country: str, zip_code: str):
    nomi = pgeocode.Nominatim(country=country)
    location = nomi.query_postal_code(zip_code)
    google_crawler = GoogleImageCrawler(storage={'root_dir': './images/'})
    google_crawler.crawl(keyword=location['community_name'], max_num=1, overwrite=True)


def mainPage():
    st.title('Main Page')
    with st.form("my_form"):
        country = st.selectbox(
        'Select Country Code',
        ('🇺🇸 United States', '🇨🇦 Canada'))
        match country:
            case '🇺🇸 United States':
                country = 'us'
            case '🇨🇦 Canada':
                country = 'ca'
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
        placeURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?location={},{}&query=beaches&key=AIzaSyAo2WOjDFJ0ELSeSblfu1cfXHnpo9u0st8".format(lat, long)
        payload={}
        headers = {}
        placeResponse = re.request("GET", placeURL, headers=headers, data=payload)
        if submitted:
            st.write("Skin Type:", option)
            st.write("You may stay outside for {} minutes".format(duration))
            st.write("Lat:", lat, "Long:", long)
            data = pd.json_normalize(json.loads(response.text))
            placeData= pd.json_normalize(json.loads(placeResponse.text))
            st.write("Current UVI", data['current.uvi'][0])
            st.write("Recommended Beaches: ")

            st.write(pd.json_normalize(placeData['results'][0])[['name', 'formatted_address']], pd.json_normalize(pd.json_normalize(placeData['results'][0])['photos'].iloc[1:20]))
            # location_image(country=country, zip_code=zip_code)
            # st.image(image='./images/000001.jpg')

            timer = st.empty()
            if isinstance(duration, int):
                secs = duration * 60
                for exposureTime in range(secs, -1, -1):
                    formatTime = time.strftime("%M:%S", time.gmtime(exposureTime))
                    timer.metric("UV Exposure Timer", formatTime)
                    time.sleep(1)
                st.warning("Timer has expired!")

page_names_to_funcs = {
    "Main Page": mainPage,
    "Skin Type Test": determineSkinType,
}

demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
