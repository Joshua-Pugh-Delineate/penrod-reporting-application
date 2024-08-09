import streamlit as st
import pandas as pd

# Set the title of the app
st.title("Preexisting Dataset Visualization")

# Path to the dataset
data_path = 'dataset/data.csv'  # Adjust the path if necessary

# Load the dataset
df = pd.read_csv(data_path)

# Display the DataFrame
st.write("Data from the preexisting dataset:")
st.dataframe(df)

# Check if the DataFrame has the required columns for a bar chart
if 'Categories' in df.columns and 'Values' in df.columns:
    # Create a bar chart
    st.bar_chart(df.set_index('Categories'))
else:
    st.error("Dataset must contain 'Categories' and 'Values' columns.")
