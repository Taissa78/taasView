# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
from streamlit_folium import st_folium
import folium

import pandas as pd

# Define variable to load the dataframe
dataframe1 = pd.read_excel("1608-rotation-2023-01-Analysis.xlsx")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

locations = dataframe1[["Time", "good_latitude", "good_longitude", "Rotation Count Value"]]

m = folium.Map(location=[40.81063, -81.39657], zoom_start=10, control_scale=True)

# If you want to dynamically add or remove items from the map,
# add them to a FeatureGroup and pass it to st_folium
fg = folium.FeatureGroup(name="State bounds")

row_ = None
for index, row in dataframe1[0:67].iterrows():
    row["good_longitude"] =  row["good_longitude"]*-1
    if row_ is None:
        previous_lat = row["good_latitude"]
        previous_lng = row["good_longitude"]
    else:
        previous_lat = row_["good_latitude"]
        previous_lng = row_["good_longitude"]
    print(index)
    print(previous_lat)
    print(previous_lng)
    print(row["Time"])
    print(row["good_latitude"])
    print(row["good_longitude"])
    print(row["good_longitude"])
    print(row["Rotation Count Value"])
    if row["Rotation Count Value"]=='rotation_count:{"N":"0"}':
        color = "orange"
    else:
        color = "blue"
    fg.add_child(
        folium.Marker(
            location=[row["good_latitude"], row["good_longitude"]],
            popup=f"{row['Time']}",
            tooltip=f"{row['Time']}",
            icon=folium.Icon(color=color, icon='glyphicon glyphicon-play-circle')
        )
    )
    fg.add_child(
        folium.PolyLine([[previous_lat, previous_lng], [row["good_latitude"], row["good_longitude"]]],
                        color=color,
                        weight=2,
                        opacity=1,
                        tooltip=f"{row['Time']}"
        )
    )
    row_ = row


out = st_folium(
    m,
    feature_group_to_add=fg,
    center="center",
    width=1200,
    height=500
)