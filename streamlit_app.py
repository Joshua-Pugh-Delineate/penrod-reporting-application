import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the app
st.title("Preexisting Dataset Visualization")

# Path to the dataset
data_path = 'dataset/penrod_daily_sales.csv'  # Adjust the path if necessary

# Initialize the DataFrame variable
df = None

# Try loading the dataset and handle potential errors
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"File not found: {data_path}")
except pd.errors.EmptyDataError:
    st.error("No data found in the file.")
except pd.errors.ParserError:
    st.error("Error parsing the file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# Proceed if DataFrame is successfully loaded
if df is not None:
    # Check if the DataFrame has the required columns for a chart
    if 'Reporting_Year' in df.columns and 'Reporting_Week' in df.columns and 'Total_Gross_Sales' in df.columns:
        # Get unique years and weeks for the filters
        years = df['Reporting_Year'].unique()
        weeks = df['Reporting_Week'].unique()

        # Sidebar filters
        st.sidebar.header("Filters")
        selected_year = st.sidebar.selectbox("Select Year", sorted(years))
        selected_week = st.sidebar.selectbox("Select Week", sorted(weeks))

        # Filter the data based on selected filters
        filtered_data = df[
            (df['Reporting_Year'] == selected_year) & 
            (df['Reporting_Week'] == selected_week)
        ]

        # Aggregate the filtered data
        aggregated_data = filtered_data.groupby(['Reporting_Year', 'Reporting_Week'])['Total_Gross_Sales'].sum().reset_index()

        # Create a line chart with Plotly
        fig = px.line(
            aggregated_data,
            x='Reporting_Week',
            y='Total_Gross_Sales',
            color='Reporting_Year',
            title='Total Gross Sales Over Reporting Weeks',
            labels={'Reporting_Week': 'Reporting Week', 'Total_Gross_Sales': 'Total Gross Sales'}
        )
        
        # Create a layout with the image and filters
        st.write("### Data Visualization")

        # Create a two-column layout: one for the image and one for the filters and chart
        col1, col2 = st.columns([1, 4])  # Adjust the ratio if needed

        with col1:
            # Display a smaller image in the top-left corner
            st.image('images/penrod_image.png', width=150)  # Replace with the path to your image and adjust width as needed

        with col2:
            # Display filters and the Plotly chart
            st.write("#### Filters")
            # Optionally, you can display the filters in the main area, but it's cleaner to keep them in the sidebar.
            st.plotly_chart(fig)

    else:
        st.error("Dataset must contain 'Reporting_Year', 'Reporting_Week', and 'Total_Gross_Sales' columns.")
