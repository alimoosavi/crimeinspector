import os
import datetime
import pandas as pd
import requests
import streamlit as st
from crime_primary_types import PRIMARY_TYPES

CRIME_INSPECTOR_BASE_URL = os.getenv('CRIME_INSPECTOR_BASE_URL')
# BASE_URL = 'http://127.0.0.1:8000'
# AUTHENTICATION_STATIC_TOKEN = 'N4rN_*!GwQUM$ggg7yxLBPru7)WBYlR9'


def fetch_crimes(primary_type: str,
                 min_date: datetime.date,
                 max_date: datetime.date
                 ):
    try:
        response = requests.get(f'{CRIME_INSPECTOR_BASE_URL}/crime/list',
                                params={'primary_type': primary_type,
                                        'min_date': min_date,
                                        'max_date': max_date})
        if not response.ok:
            raise Exception()

        results = response.json()['results']
        return [[item['latitude'], item['longitude']]
                for item in results
                ]
    except Exception:
        return []


primary_type = st.sidebar.selectbox('Crime Primary Type', PRIMARY_TYPES)
min_date = st.sidebar.date_input('Crime Min Date')
max_date = st.sidebar.date_input('Crime Max Date')

map_data = pd.DataFrame(fetch_crimes(primary_type=primary_type,
                                     min_date=min_date,
                                     max_date=max_date), columns=['lat', 'lon'])
st.map(map_data)
