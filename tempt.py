import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import joblib

st.title('Location Temperature Prediction')
# Create a file uploader widget
file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    # Load data from the uploaded file
    data = pd.read_csv(file)

    # Display the data in Streamlit
    st.write(data)

    # Add a "Predict" button
    if st.button("Predict"):
        # Load model
        model = joblib.load('/Users/rianrachmanto/pypro/project/model/model_rfs.joblib')

        # Make predictions on the new data
        predictions = model.predict(data)

        # Add the predictions as a new column to the DataFrame
        data["predictions"] = predictions

        # Display the updated DataFrame with predictions
        st.write(data)
 # Create a folium map centered at the mean latitude and longitude values
    mean_lat = data["lat"].mean()
    mean_lon = data["lon"].mean()
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=10, tiles="OpenStreetMap")

    # Convert the latitude and longitude data into a list of points
    heat_data = data[["lat", "lon"]].values.tolist()

    # Create a HeatMap layer with the list of points
    heat_layer = HeatMap(heat_data, radius=15, blur=10)

    # Add the HeatMap layer to the map
    heat_layer.add_to(m)

    # Display the map using the st_folium command
    folium_static(m)