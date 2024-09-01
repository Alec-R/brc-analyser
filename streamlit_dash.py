import streamlit as st
import pandas as pd
import plotly.express as px
import yf_utils as yfu

def load_data():
    pct_fields = yfu.get_pct_fields()
    largenum_fields = yfu.get_largenum_fields()
    df = yfu.create_dataframe(yfu.fetch_data(yfu.get_tickers(),yfu.get_fields()))
    return df

def load_csv():
    return pd.read_csv('stock_data.csv')

def main():
    st.title('Stock Data Dashboard')

    # Load the data
    df = load_data()

    styled_df = yfu.format_dataframe(df, yfu.get_pct_fields(), yfu.get_largenum_fields())

    # Display the raw data
    st.subheader('Raw Data')
    st.dataframe(df)

    # Allow user to select a numeric column for visualization
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    selected_column = st.selectbox('Select a column to visualize:', numeric_columns)

    # Create a bar chart of the selected column
    fig = px.bar(df, x='Ticker', y=selected_column, title=f'{selected_column} by Ticker')
    st.plotly_chart(fig)

    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(df.describe())

    # Allow user to filter data
    st.subheader('Filter Data')
    min_value = float(df[selected_column].min())
    max_value = float(df[selected_column].max())
    filter_value = st.slider(f'Filter {selected_column}', min_value, max_value, (min_value, max_value))
    filtered_df = df[(df[selected_column] >= filter_value[0]) & (df[selected_column] <= filter_value[1])]
    st.dataframe(filtered_df)

if __name__ == '__main__':
    main()