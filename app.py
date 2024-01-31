import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Page icons https://webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Athena Books',
                   page_icon=':books:')

# URL of the public spreadsheet
url = "https://docs.google.com/spreadsheets/d/17D4Xkbt9jpDO24AfpsHQrhw1gyrv_6Wcd6oiLFdW9GY/edit?usp=sharing"

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
df = conn.read(
  spreadsheet=url,
  worksheet="sheet1",
  ttl="5"
)

# Drop rows where all elements are missing
df = df.dropna(how='all')

# Drop columns where all elements are missing
df = df.dropna(axis=1, how='all')

st.dataframe(df, hide_index=True)
