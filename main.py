# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import geopy.distance
import math
import re



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


def find_dots(initial, last):
    previous_row = None
    total_miles_driven = 0
    total_mileage_in_revolution = 0
    # print(initial, last)
    for index, row in dataframe1[initial:last+1].iterrows():
        if not math.isnan(row["good_longitude"]) and not math.isnan(row["good_latitude"]):
            if row["Rotation Count Value"] == 'rotation_count:{"N":"0"}':
                color_icon = "orange"
                color_line = "orange"
            else:
                color_icon = "blue"
                color_line = "blue"

            if previous_row is None:
                previous_lat = row["good_latitude"]
                previous_lng = row["good_longitude"]
                first_date = row["Time"]
                previous_rev_json = row["Rotation Count Value"]
                color_icon = "green"
            else:
                previous_lat = previous_row["good_latitude"]
                previous_lng = previous_row["good_longitude"]
                previous_rev = previous_row["Rotation Count Value"]
                if index == int(last):
                    last_date = row["Time"]
                    color_icon = "black"


            # print(index)
            # print(previous_lat)
            # print(previous_lng)
            # print(row["Time"])
            # print(row["good_latitude"])
            # print(row["good_longitude"])
            # print(row["good_longitude"])
            # print(row["Rotation Count Value"])

            rotation_count_group = re.search(r'\d+', row["Rotation Count Value"])
            previous_rotation_count_group = re.search(r'\d+', previous_rev_json)
            rotation_count = int(rotation_count_group.group())
            previous_rotation_count = int(previous_rotation_count_group.group())

            if rotation_count == 0 and previous_rotation_count > 0:
                rotation_count = previous_rotation_count
            elif rotation_count > 0 and previous_rotation_count == 0:
                previous_rotation_count = rotation_count

            difference_revolution = rotation_count - previous_rotation_count
            mileage_in_revolution = difference_revolution / 485

            # simulate odometer reading
            miles_driven = geopy.distance.distance([previous_lat, previous_lng],
                                                   [row["good_latitude"], row["good_longitude"]]).miles
            total_miles_driven = miles_driven + total_miles_driven
            print(mileage_in_revolution, total_mileage_in_revolution)
            total_mileage_in_revolution = mileage_in_revolution + total_mileage_in_revolution

            fg.add_child(
                folium.Marker(
                    location=[row["good_latitude"], row["good_longitude"]],
                    popup=f"<b>{row['Time']}</b><br>"
                          f"Point index: <b>{index}</b><br>"
                          f"Rotation Count: <b>{rotation_count}</b><br>"
                          f"Rotation Difference: <b>{difference_revolution}</b><br>"
                          f"Path Miles Driven: <b>{miles_driven}</b><br>"
                          f"Path Revolution Miles: <b>{mileage_in_revolution}</b><br>"
                          f"Total Miles Driven <b>{total_miles_driven}</b><br>"
                          f"Total Revolution Mileage: <b>{total_mileage_in_revolution}</b><br>",
                    tooltip=f"<b>{row['Time']}</b><br>"
                          f"Point index: <b>{index}</b><br>"
                          f"Rotation Count: <b>{rotation_count}</b><br>"
                          f"Rotation Difference: <b>{difference_revolution}</b><br>"
                          f"Path Miles Driven: <b>{miles_driven}</b><br>"
                          f"Path Revolution Miles: <b>{mileage_in_revolution}</b><br>"
                          f"Total Miles Driven <b>{total_miles_driven}</b><br>"
                          f"Total Revolution Mileage: <b>{total_mileage_in_revolution}</b><br>",
                    icon=folium.Icon(color=color_icon, icon='glyphicon glyphicon-play-circle')
                )
            )
            fg.add_child(
                folium.PolyLine([[previous_lat, previous_lng], [row["good_latitude"], row["good_longitude"]]],
                                color=color_line,
                                weight=2,
                                opacity=1,
                                tooltip=f"{row['Time']}"
                )
            )
            previous_row = row


#find_dots(0, 297)

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    initial_index = st.text_input(
        "Initial Index",
        #label_visibility=st.session_state.visibility,
        #disabled=st.session_state.disabled,
        #placeholder=dataframe1.loc[0].at["Time"],
    )

    if initial_index:
        st.write("You entered: ", initial_index, dataframe1.loc[int(initial_index)].at["Time"])
        #dataframe1[dataframe1.eq(initial_date).any(1)

with col2:
    final_index = st.text_input(
        "Final Index",
        #label_visibility=st.session_state.visibility,
        #disabled=st.session_state.disabled,
        #placeholder=dataframe1.loc[297].at["Time"],
    )

    if final_index:
        st.write("You entered: ", final_index, dataframe1.loc[int(final_index)].at["Time"])
        #final_date_index = dataframe1[dataframe1.eq(final_date).any(1)].index.tolist()[0]
        find_dots(int(initial_index), int(final_index))


out = st_folium(
    m,
    feature_group_to_add=fg,
    center="center",
    width=1200,
    height=500
)