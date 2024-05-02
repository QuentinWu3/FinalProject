"""
Name: Quentin Wu
CS230: Section 6
Data: Rest Areas in California
URL: Link to your web application on Streamlit Cloud (if posted)

Description: This program have 4 seperate sections. The first part maps out all the rest areas in california with markers
which allows use to hover and view basic information of the rest area. This is followed by a piechart that shows the
number of rest areas in each district. There is also one query which allows user to select the rest area and displays
available amenities in the rest area as well as another query which allows user to input a specific route and outputs
the available rest areas on the specific route.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

dfRestArea = pd.read_csv("Rest_Areas.csv", index_col="OBJECTID")


# function that creates and plots rest areas all over california [VIZ4]
def plotmap(df):
    columns = ["NAME", "ADDRESS", "CITY",
               "ZIPCODE", "LATITUDE", "LONGITUDE", "REST_AREA"]  # columns relevant for plotting the map
    dfMap = df.loc[:, columns]  # creating new df with the only columns[DA7]

    # primary view of the map when the application first starts up
    view = pdk.ViewState(
        latitude=dfMap["LATITUDE"].mean(),
        longitude=dfMap["LONGITUDE"].mean(),
        zoom=5,
        pitch=0
    )

    # plotting datapoints on map
    layer1 = pdk.Layer(
        "ScatterplotLayer",
        data=dfMap,
        get_position=["LONGITUDE", "LATITUDE"],
        get_radius=25,
        auto_highlight=True,
        get_color=[50, 100, 200],
        radius_min_pixels=5,
        pickable=True
    )

    # tooltip when hovering over datapoints [PY5]
    tool_tip = {"html":
                    "Name: <b>{REST_AREA}</b></br>"
                    "Address: <b>{ADDRESS}</b></br>"
                    "City: <b>{CITY}</b></br>"
                    "Zip: <b>{ZIPCODE}</b></br>",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }

    # creating map
    restmap = pdk.Deck(
        map_style="light",
        initial_view_state=view,
        layers=layer1,
        tooltip=tool_tip
    )

    # plotting map with streamlit [ST1]
    st.pydeck_chart(restmap)


# function that displays a pie_chart which compares the amount of rest areas in each county [VIZ1]
def piechart(df):
    # groups data by district
    DistrictNum = df.groupby("DISTRICT").size().reset_index(name="count")
    # It creates a pie chart to represent the distribution of rest areas across different districts.
    fig, ax = plt.subplots()
    # The explode effect highlights the district with the highest number of rest areas in the pie chart.
    max_index = DistrictNum["count"].idxmax()
    explode = [0.1 if i == max_index else 0 for i in range(len(DistrictNum))]
    ax.pie(DistrictNum["count"], labels=DistrictNum["DISTRICT"], explode=explode, labeldistance=1.1, autopct="%1.0f%%",
           pctdistance=0.75, startangle=90)

    st.header(":blue[Pie Chart Displaying Percentage of Rest Areas in each District]", divider="grey")
    st.pyplot(fig) # [ST2]


# function which retrieves the values in Rest_area and return them into a list [PY4]
def restArea(df, column="REST_AREA"):
    restArea = df[column].unique().tolist()
    return restArea


# function which creates a select box that allows user to select a rest area and displays a table with the available amenities [PY1][DA4]
def filterByRestArea(restArea):
    st.header(":blue[Available Amenities in Rest Area]", divider="grey") #[ST4]
    # creates select box with all unique rest area names [ST3][DA2]
    ra = st.selectbox(
        "Select a Rest Area:",
        sorted(restArea),
        index=None
    )

    st.write('Amenities in', ra, ":")

    # select column headers and locate rows containing the selected city [VIZ2]
    dfra = dfRestArea.loc[:,
           ["REST_AREA", "RESTROOM", "WATER", "PICNICTAB", "PHONE", "HANDICAP", "RV_STATION", "VENDING", "PET_AREA"]]
    dfra = dfra.loc[dfra["REST_AREA"] == ra]

    st.dataframe(dfra)


# function that displays in a table, available rest areas on a given route [VIZ3]
def get_rest_areas_on_route(route_number):
    return dfRestArea[dfRestArea["ROUTE"] == route_number][["REST_AREA", "ADDRESS", "CITY"]]

# [PY2]
def main(rest_areas=None, route_number=None):
    st.title("Rest areas in California")

    st.header(":blue[All Rest Areas in California]", divider="grey")
    plotmap(dfRestArea)

    piechart(dfRestArea)

    filterByRestArea(restArea(dfRestArea))

    st.header(":blue[Rest Areas on Route Finder]", divider="grey")
    route_input = st.text_input("Enter Route Number:")
    valid_route_numbers = dfRestArea["ROUTE"]
    if st.button("Find Rest Areas"):
        if route_input:
            route_number = int(route_input)
            if route_number in valid_route_numbers:
                st.write("Invalid Route, Please Try Again.")
            else:
                rest_areas = get_rest_areas_on_route(route_number)
                st.write(rest_areas)


if __name__ == "__main__":
    main()
