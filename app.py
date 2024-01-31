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
st.sidebar.header('Please Filter Here:')

# Combine author and title lists
combined_list = ['All'] + df['Author'].unique().tolist() + df['Title'].unique().tolist()
selected_option = st.sidebar.selectbox('Select an Author or Book Title', combined_list)

# Filtering the DataFrame based on selection
if selected_option in df['Author'].unique():
    df_selection = df[df['Author'] == selected_option]
elif selected_option in df['Title'].unique():
    df_selection = df[df['Title'] == selected_option]
else:
    df_selection = df

# Display the DataFrame
st.dataframe(df_selection, hide_index=True)

