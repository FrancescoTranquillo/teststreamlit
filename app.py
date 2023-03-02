import streamlit as st
import pandas as pd

# Set the title and sidebar layout of the app
st.set_page_config(page_title="Excel Dashboard", layout="wide")

# Set the title of the app
st.title("Excel Dashboard")

# Allow the user to upload a file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# If a file has been uploaded
if uploaded_file is not None:
    # Load the Excel file into a Pandas dataframe
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Display the raw data
    st.write("Raw Data")
    st.write(df)

    # Display some basic statistics about the data
    st.write("Basic Statistics")
    st.write(df.describe())

    # Display a bar chart of the data
    st.write("Bar Chart")
    st.bar_chart(df)

    # Display a line chart of the data
    st.write("Line Chart")
    st.line_chart(df)

    # Display an area chart of the data
    st.write("Area Chart")
    st.area_chart(df)
