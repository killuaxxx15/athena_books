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
  usecols=[0, 1, 2]
)

# Drop rows where all elements are missing
df = df.dropna(how='all')

# Drop columns where all elements are missing
df = df.dropna(axis=1, how='all')





# Function to create clickable links
def make_clickable(link, text="Link"):
    return f'<a target="_blank" href="{link}">{text}</a>'

# Sidebar for filter options
st.sidebar.header('Please Filter Here:')

# Function to reset title selection
def reset_title():
    st.session_state.selected_title = 'All'

# Function to reset author selection
def reset_author():
    st.session_state.selected_author = 'All'

# Dropdown to select an author
author_list = ['All'] + sorted(df['Author'].unique().tolist())
if 'selected_author' not in st.session_state:
    st.session_state['selected_author'] = 'All'
selected_author = st.sidebar.selectbox('Select an Author', author_list, on_change=reset_title, key='selected_author')

# Dropdown to select a book title
title_list = ['All'] + sorted(df['Title'].unique().tolist())
if 'selected_title' not in st.session_state:
    st.session_state['selected_title'] = 'All'
selected_title = st.sidebar.selectbox('Select a Book Title', title_list, on_change=reset_author, key='selected_title')

# Filtering the DataFrame based on selection
if selected_author != 'All':
    df_selection = df[df['Author'] == selected_author]
elif selected_title != 'All':
    df_selection = df[df['Title'] == selected_title]
else:
    df_selection = df

# Check if 'Link' column exists before modifying it
if 'Link' in df_selection.columns:
    df_selection['Link'] = df_selection['Link'].apply(lambda x: make_clickable(x))
    # Display the DataFrame with HTML rendering for links
    st.markdown(df_selection.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.error("Link column not found in the DataFrame.")
