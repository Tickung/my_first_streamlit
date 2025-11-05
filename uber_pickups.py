import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from numpy.random import default_rng as rng
import plotly.graph_objects as go
import plotly.express as px
from IPython.display import HTML

st.title('Streamlit Learning')
df = pd.read_csv("https://raw.githubusercontent.com/Tickung/DADS5001/refs/heads/main/premier_league.csv")
# Dictionary of team names to logo URLs (example - actual URLs may vary and need updating)
team_logo_urls = {
    'Arsenal': 'https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg',
    'Bournemouth': 'https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg',
    'Tottenham': 'https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg',
    'Sunderland': 'https://upload.wikimedia.org/wikipedia/hif/e/e0/Logo_Sunderland.png',
    'Manchester City': 'https://upload.wikimedia.org/wikipedia/sco/e/eb/Manchester_City_FC_badge.svg',
    'Manchester Utd': 'https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg',
    'Liverpool': 'https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg',
    'Aston Villa': 'https://upload.wikimedia.org/wikipedia/hif/5/57/Aston_Villa.png',
    'Chelsea': 'https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg',
    'Newcastle Utd': 'https://upload.wikimedia.org/wikipedia/hif/2/25/Newcastle_United_Logo.png',
    'Brentford': 'https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg',
    'Brighton': 'https://upload.wikimedia.org/wikipedia/sco/f/fd/Brighton_%26_Hove_Albion_logo.svg',
    'Crystal Palace': 'https://upload.wikimedia.org/wikipedia/sco/0/0c/Crystal_Palace_FC_logo.svg',
    'Everton': 'https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg',
    'Leeds United': 'https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg',
    'Burnley': 'https://upload.wikimedia.org/wikipedia/en/6/6d/Burnley_FC_Logo.svg',
    'Fulham': 'https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg',
    'Nott\'ham Forest': 'https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg',
    'West Ham': 'https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg',
    'Wolves': 'https://upload.wikimedia.org/wikipedia/sco/f/fc/Wolverhampton_Wanderers.svg'
}

# Add the logo URLs to the dataframe
df['Logo_URL'] = df['Squad'].map(team_logo_urls)
def path_to_image_html(path):
    return f'<img src="{path}" width="30" >'

# Apply the function to the 'Logo_URL' column and display the table
df_html = df.to_html(escape=False, formatters=dict(Logo_URL=path_to_image_html))

st.components.v1.html(df_html, height=300, scrolling=True)


st.dataframe(df.head())
fig = px.scatter(df,
                 x="xG",
                 y="xGA",
                 size="Pts",
                 hover_name="Squad",
                 title="xG vs. xGA with Pts as Bubble Size (Plotly)")

st.plotly_chart(fig, use_container_width=True)



st.subheader('Learning section')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

st.subheader('Raw data')
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
# st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')

st.map(filtered_data)


