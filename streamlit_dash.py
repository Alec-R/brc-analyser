import streamlit as st
import pandas as pd
import plotly.express as px
import yf_utils as yfu

def load_data():
    """ TODO refactor to a data handler class which returns the df? """
    df = yfu.create_dataframe(yfu.fetch_data(yfu.get_tickers(),yfu.get_fields()))
    return df


def load_csv():
    return pd.read_csv('stock_data.csv')

def df_calculatins(df) -> pd.DataFrame:
    input_barrier = 0.55
    input_coupon = 0.12
    # creates a dict with all the tickers for the manual EPS input 

    # inputs
    # df.join(input_eps,on='Ticker')
    df['eps_projected_manual'] = 1

    ## calculations
    # recalculate the price to earnings to check
    df['trailing_calc_pe_check'] = ( (df['currentPrice'] / df['trailingEps']) != df['trailingPE'] )
    # projected eps growth
    df['projected_eps_growth'] = (df['forwardEps'] / df['trailingEps']  - 1 )
    # the price at barrier level
    df['price_exbarrier'] = df['currentPrice'] * input_barrier
    # the new PE if the price is at barrier level
    df['drawdown_pe'] = df['price_exbarrier'] / df['trailingEps']
    # the new projected PE if the price is at barrier level - consensus eps projection from yfinance 
    df['drawdown_pe_projected'] = df['price_exbarrier'] / df['forwardEps']
    # the new projected PE if the price is at barrier level - manual eps input
    df['drawdown_pe_projected_manual'] = df['price_exbarrier'] / df['eps_projected_manual']
    # price to mean target percentage diff
    df['price_to_targetprice'] = ( df['currentPrice'] / df['targetMeanPrice'] ) - 1

    return df


def main():

    st.title('Stock Data Dashboard - Beta')
    st.write(
        """ Data is preloaded from YFinance. 

        Usage:

        1. Select the tickers in the sidebar
        1. Input the BRC characteristics
        1. Input the stock specific assumptions in the data editor
        1. Click "recalculate" to display results when changing assumptions

        """
    )
    st.header('BRC Characteristics'
              )
    st.header('Data editor')
    # Load the data
    df = load_data()
    # df = df.set_index('Ticker')
    df = df_calculatins(df)
    st.data_editor(df)

    # sidebar ===================
    st.sidebar.header('Stock picker')
    # BRC list
    selected_list = st.sidebar.selectbox('Select Ticker List', df['Ticker'].tolist())
    
    # Display and edit selected ticker list
    selected_tickers = st.sidebar.multiselect('Edit Ticker List', df['Ticker'].tolist(), default=df['Ticker'].tolist())
    
    """
    if st.sidebar.button('Save Ticker List'):
        ticker_lists[selected_list] = selected_tickers
        save_ticker_lists(ticker_lists)
        st.sidebar.success(f'Saved {selected_list}')
    # Filter dataframe based on selected tickers
    df_filtered = df[df['Ticker'].isin(selected_tickers)]
    """

    # tabs ===================
    tab_names = ["Overview", "Fundamentals", "Forward View"]
    sections_fieldlist = yfu.get_sectionfields()
    tab1, tab2, tab3 = st.tabs(tab_names)

    with tab1:
        tab_name = tab_names[0]
        tab_df = df[sections_fieldlist[tab_name]]
        tab_df_styled = yfu.format_dataframe(tab_df)
        st.header(tab_name)
        st.dataframe(tab_df_styled)

    with tab2:
        tab_name = tab_names[1]
        tab_df = df[sections_fieldlist[tab_name]]
        tab_df_styled = yfu.format_dataframe(tab_df)
        st.header(tab_name)
        st.dataframe(tab_df_styled)
        
        # Financial charts
        fig1 = px.bar(tab_df, x='Ticker', y='trailingPE')
        st.plotly_chart(fig1)
        
        fig2 = px.bar(tab_df, x='Ticker', y='trailingEps')
        st.plotly_chart(fig2)

    with tab3:
        tab_name = tab_names[2]
        tab_df = df[sections_fieldlist[tab_name]]
        # tab_df_styled = yfu.format_dataframe(tab_df)        
        st.header(tab_name)
        st.dataframe(tab_df)
        
        # Market data charts
        fig3 = px.scatter(tab_df, x='trailingPE', y='price_to_targetprice', size='pegRatio', 
                          hover_name='Ticker', title='P/E Ratio vs Payout, size is peg')
        st.plotly_chart(fig3)


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