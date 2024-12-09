import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import pydeck as pdk

# Load trade data
@st.cache
def load_data():
    trade_data = pd.read_csv('data/trade_data.csv')
    countries_map = gpd.read_file('data/countries_map.geojson')
    return trade_data, countries_map

# Load data
trade_data, countries_map = load_data()

# Title and description
st.title('Middle East Economic Trade Routes & Dependencies')
st.markdown("""
This app visualizes the economic trade routes and dependencies in the Middle East, 
showing how different countries interact in terms of trade, partnerships, and economic 
flow based on historical and current data.
""")

# Map selection
st.sidebar.header('Filters')
selected_country = st.sidebar.selectbox('Select Country', trade_data['Country'].unique())

# Filter trade data by selected country
filtered_data = trade_data[trade_data['Country'] == selected_country]

# Display trade data table
st.subheader(f'Trade Data for {selected_country}')
st.write(filtered_data)

# Visualize trade routes on the map using PyDeck (with trade data)
st.subheader('Economic Trade Routes')
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=filtered_data['Latitude'].mean(),
        longitude=filtered_data['Longitude'].mean(),
        zoom=5,
        pitch=45,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            filtered_data,
            get_position='[Longitude, Latitude]',
            get_radius=200000,
            get_color='[255, 0, 0]',
            pickable=True,
        ),
    ],
)

st.pydeck_chart(deck)

# Plot trade volume by country using Plotly
st.subheader('Trade Volume by Country')
trade_volume = filtered_data.groupby('Trade_Partner')['Trade_Volume'].sum().reset_index()
fig = px.bar(trade_volume, x='Trade_Partner', y='Trade_Volume', title=f'Trade Volume for {selected_country}')
st.plotly_chart(fig)

# Map of countries with trade dependencies
st.subheader('Trade Dependencies in the Middle East')
st.write('The map below shows trade routes across the Middle East.')
fig_map = px.choropleth(
    countries_map,
    geojson=countries_map.geometry,
    locations=countries_map.index,
    color=trade_data.groupby('Country')['Trade_Volume'].sum(),
    color_continuous_scale="Viridis",
    labels={'Trade_Volume': 'Total Trade Volume'},
    title="Trade Dependencies Across the Middle East"
)

fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map)

# Conclusion
st.markdown("""
By exploring this visualization, you can better understand the intricate economic 
trade routes and dependencies that shape international relations in the Middle East. 
The interactive features allow for a deep dive into specific countries and trade patterns.
""")
