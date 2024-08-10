import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the app
st.title("Preexisting Dataset Visualization")

# Path to the dataset
data_path = 'dataset/penrod_sales_all_years.csv'  # Adjusted to the new dataset name

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
    if 'Reporting_Year' in df.columns and 'Reporting_Week' in df.columns and 'Total_Gross_Sales' in df.columns and 'Tickets_Sold' in df.columns:
        # Ensure Reporting_Year is treated as a categorical variable
        df['Reporting_Year'] = df['Reporting_Year'].astype(str)

        # Get unique years and weeks for the filters
        years = df['Reporting_Year'].unique()
        weeks = df['Reporting_Week'].unique()

        # Top Section: Key Metrics and Penrod Image
        st.write("### Data Visualization")

        # Create a container for the top section
        top_container = st.container()
        with top_container:
            # Define columns layout with sufficient spacing
            top_col1, top_col2 = st.columns([2, 3], gap="large")  # Adjusted ratios with large gap

            with top_col1:
                # Display a large image with padding
                st.image('images/penrod_image.png', width=300)

            with top_col2:
                # Create a container for the cards with sufficient spacing
                st.write("#### Key Metrics")
                with st.container():
                    card_col1, card_col2 = st.columns([1, 1], gap="large")  # Two columns for cards with large gap

                    with card_col1:
                        # Total Gross Sales Card
                        total_sales = df['Total_Gross_Sales'].sum()
                        total_sales_card = f"""
                        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); text-align: center;">
                            <h3 style="margin: 0; color: #333;">Total Gross Sales</h3>
                            <h2 style="margin: 0; color: #333;">${total_sales:,.2f}</h2>
                        </div>
                        """
                        st.markdown(total_sales_card, unsafe_allow_html=True)

                    with card_col2:
                        # Tickets Sold Card
                        tickets_sold = df['Tickets_Sold'].sum()
                        tickets_sold_card = f"""
                        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); text-align: center;">
                            <h3 style="margin: 0; color: #333;">Tickets Sold</h3>
                            <h2 style="margin: 0; color: #333;">{tickets_sold:,}</h2>
                        </div>
                        """
                        st.markdown(tickets_sold_card, unsafe_allow_html=True)

        # Middle Section: Filters
        st.write("### Filters")

        filter_col1, filter_col2 = st.columns([1, 1], gap="large")  # Adjust column width ratios with large gap

        with filter_col1:
            # Drop-down for 'All' years and weeks
            filter_option = st.radio(
                "Filter By",
                options=["All", "Multiple"],
                horizontal=True  # Display options horizontally
            )

            if filter_option == "All":
                # Drop-down for 'All' years and weeks
                selected_years = st.multiselect(
                    "Select Year(s)",
                    options=['All'] + sorted(years.tolist()),
                    default=['All'],
                    key="year_filter",
                    placeholder="Select year(s)"
                )
                selected_weeks = st.multiselect(
                    "Select Week(s)",
                    options=['All'] + sorted(weeks.tolist()),
                    default=['All'],
                    key="week_filter",
                    placeholder="Select week(s)"
                )
                if 'All' in selected_years:
                    selected_years = years.tolist()
                if 'All' in selected_weeks:
                    selected_weeks = weeks.tolist()

            elif filter_option == "Multiple":
                # Multi-select for multiple years and weeks
                selected_years = st.multiselect(
                    "Select Year(s)",
                    options=sorted(years.tolist()),
                    key="year_filter",
                    placeholder="Select year(s)"
                )
                selected_weeks = st.multiselect(
                    "Select Week(s)",
                    options=sorted(weeks.tolist()),
                    key="week_filter",
                    placeholder="Select week(s)"
                )

        # Filter the data based on selected filters
        filtered_data = df[
            (df['Reporting_Year'].isin(selected_years) if selected_years else True) & 
            (df['Reporting_Week'].isin(selected_weeks) if selected_weeks else True)
        ]

        # Aggregate the filtered data if it is not empty
        if not filtered_data.empty:
            # Aggregate data separately for each metric
            aggregated_sales = filtered_data.groupby(['Reporting_Year', 'Reporting_Week'])['Total_Gross_Sales'].sum().reset_index()
            aggregated_tickets = filtered_data.groupby(['Reporting_Year', 'Reporting_Week'])['Tickets_Sold'].sum().reset_index()

            # Bottom Section: Bar Charts
            st.write("### Total Gross Sales and Tickets Sold by Reporting Week")

            # Bar Chart for Total Gross Sales
            fig_sales = px.bar(
                aggregated_sales,
                x='Reporting_Week',
                y='Total_Gross_Sales',
                color='Reporting_Year',
                title='Total Gross Sales by Reporting Week',
                labels={'Reporting_Week': 'Reporting Week', 'Total_Gross_Sales': 'Total Gross Sales'},
                height=400
            )
            st.plotly_chart(fig_sales, use_container_width=True)

            # Bar Chart for Tickets Sold
            fig_tickets = px.bar(
                aggregated_tickets,
                x='Reporting_Week',
                y='Tickets_Sold',
                color='Reporting_Year',
                title='Tickets Sold by Reporting Week',
                labels={'Reporting_Week': 'Reporting Week', 'Tickets_Sold': 'Tickets Sold'},
                height=400
            )
            st.plotly_chart(fig_tickets, use_container_width=True)

        else:
            st.write("No data available for the selected filters.")

    else:
        st.error("Dataset must contain 'Reporting_Year', 'Reporting_Week', 'Total_Gross_Sales', and 'Tickets_Sold' columns.")
