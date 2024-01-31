import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Page icons https://webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Athena Books',
                   page_icon=':books:')

# URL of the public spreadsheet
url = "https://docs.google.com/spreadsheets/d/17D4Xkbt9jpDO24AfpsHQrhw1gyrv_6Wcd6oiLFdW9GY/edit?usp=sharing"

# Create a connection object
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
df = conn.read(
  spreadsheet=url,
  usecols=[0, 1]
)

# Drop rows where all elements are missing
df = df.dropna(how='all')

# Drop columns where all elements are missing
df = df.dropna(axis=1, how='all')

# st.dataframe(df, hide_index=True)

# Sidebar for filter options
st.sidebar.header('Filter Options')

# Dropdown to select an author
author_list = ['All'] + df['Author'].unique().tolist()
selected_author = st.sidebar.selectbox('Select an Author', author_list)

# Dropdown to select a book title
title_list = ['All'] + df['Title'].unique().tolist()
selected_title = st.sidebar.selectbox('Select a Book Title', title_list)

# Constructing the query string based on user selection
query_str = []

if selected_author != 'All':
    query_str.append(f"author == '{selected_author}'")
if selected_title != 'All':
    query_str.append(f"title == '{selected_title}'")

query_str = " & ".join(query_str)

# Applying the query if any filter is selected, else display original dataframe
filtered_df = df.query(query_str) if query_str else df

# Display DataFrame in the main page
st.dataframe(filtered_df, hide_index=True)
