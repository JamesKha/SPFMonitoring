from pyrsistent import s
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
        hair = st.selectbox(
            'Select hair color',
            ("blond", "dark blond",  "brown", "dark brown", "black"))
        eyeColor = st.selectbox(
            'Select eye color',
            ("blue", "gray",  "brown", "dark brown"))
        submitted = st.form_submit_button("Submit")

        type = 'V'
        match skin:
            case "very light":
                type = "I"
            case "light":
                if (eyeColor == "gray") or (eyeColor == "brown"):
                    type = "III"
                else:
                    type = "II"
            case "light brown":
                if (hair in ["dark brown", "black"]):
                    type = "IV"
                else:
                    type = "III"
            case "olive-colored":
                type = "IV"
            case "dark brown":
                if (hair == "black") and (eyeColor == "dark brown"):
                    type = "V"
            case "black":
                type = "VI"
            case _:
                type = "V"
        if submitted:
            st.write("Skin Type:", type)




def mainPage():
    st.title('Beach Day Planner')
    with st.form("my_form"):
        country = st.selectbox(
            'Select Country Code',
            ('🇺🇸 United States', '🇨🇦 Canada'))
        match country:
            case '🇺🇸 United States':
                country = 'us'
            case '🇨🇦 Canada':
                country = 'ca'
        zip_code = st.text_input(label="ZIP/Postal Code",  disabled=False)
        nomi = pgeocode.Nominatim(country)
        nomi_respository = nomi.query_postal_code(zip_code)
        lat, long = nomi_respository['latitude'], nomi_respository['longitude']
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

        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}".format(
            lat, long, st.secrets["weather_key"])
        payload = {}
        headers = {}
        response = re.request("GET", url, headers=headers, data=payload)
        placeURL = "https://maps.googleapis.com/maps/api/place/textsearch/json?location={},{}&query=beaches&key={}".format(
            lat, long, st.secrets["google_key"])
        payload = {}
        headers = {}
        placeResponse = re.request(
            "GET", placeURL, headers=headers, data=payload)
        if submitted:
            st.write("Skin Type:", option)
            st.write("You may stay outside for {} minutes".format(duration))
            st.write("Lat:", lat, "Long:", long)
            data = pd.json_normalize(json.loads(response.text))
            placeData = pd.json_normalize(json.loads(placeResponse.text))
            st.write("Current UVI", data['current.uvi'][0])
            strCol = pd.json_normalize(pd.json_normalize(placeData['results'][0])['photos'].iloc[1:20].str[0] ).photo_reference.apply(lambda x: st.image('https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=' + str(x) + '&key=' + st.secrets["google_key"]))
            st.write("Recommended Beaches: ")
            st.write(pd.json_normalize(placeData['results'][0])[['name', 'formatted_address']],strCol)

            mapData = {
                'name': [],
                'lat': [],
                'lon': []
            }
            for each in placeData['results'][0]:
                mapData['name'].append(each['name'])
                mapData['lat'].append(each['geometry']['location']['lat'])
                mapData['lon'].append(each['geometry']['location']['lng'])
            st.write("Map of nearby beaches:")
            df = pd.DataFrame(mapData)
            st.map(df)

            timer = st.empty()
            if isinstance(duration, int):
                secs = duration * 60
                for exposureTime in range(secs, -1, -1):
                    formatTime = time.strftime(
                        "%M:%S", time.gmtime(exposureTime))
                    timer.metric("UV Exposure Timer", formatTime)
                    time.sleep(1)
                st.warning("Timer has expired!")


page_names_to_funcs = {
    "Main Page": mainPage,
    "Skin Type Test": determineSkinType,
}

demo_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
