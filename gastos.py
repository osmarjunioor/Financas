#python -m streamlit run 1_Links.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Vendor Management Portal")
st.markdown("Enter the details of the new vendor below.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors")
existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)