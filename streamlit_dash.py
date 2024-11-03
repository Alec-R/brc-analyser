import streamlit as st
import pandas as pd
import plotly.express as px
import yf_utils as yfu
from yf_config import DEFAULT_BARRIER, DEFAULT_COUPON

def display_metrics(metrics,df):
    for metric in metrics:
            fig = px.strip(df, x=metric, hover_data=['Ticker'],title=metric, color='Ticker' )
            # Customize the layout to make it very compact
            fig.update_layout(
                height=100,  # Minimal height
                showlegend=False,                
                yaxis={'showticklabels': True, 'showgrid': True, 'zeroline': False},
                xaxis={'title': ''},
                margin={'l': 40, 'r': 40, 't': 30, 'b': 20},
                title={
                     'text': metric,
                     'y':0.8,
                     'x':0.01,
                     'font':{'size':14},
                     'xanchor': 'left',
                     'yanchor': 'top'
                     }
                     )
            st.plotly_chart(fig)    

def main():
    session_handler = yfu.DataHandler()
    df = session_handler.df

    st.title('Stock Data Dashboard - Beta')
    st.write(
        """ Data is preloaded from YFinance. 

        Usage:

        1. Select the tickers in the sidebar
        2. Input the BRC characteristics (barrier)
        3. Input the stock specific assumptions in the data editor
        4. Click "recalculate" to display results when changing assumptions

        """
    )

    st.header('BRC Characteristics')
    # Load the data
    # df = df.set_index('Ticker')

    # ===================
    # sidebar 
    # ===================
    st.sidebar.header('Stock picker')

    barrier = st.sidebar.number_input(
        "Product barrier - percent: ", 
        placeholder="Type a number in percent...",
        value=DEFAULT_BARRIER,
        min_value=1.0 )

    session_handler.df_calculations(barrier)
    
    st.write(" // QA DF check")
    st.write(df)
    st.write(" // QA DF check")


    # Display and edit selected ticker list
    selected_tickers = st.sidebar.multiselect('Edit Ticker List', df['Ticker'].tolist(), default=df['Ticker'].tolist())


    # ===================
    # tabs 
    # ===================
    tab_names = ["Overview", "Fundamentals", "Forward View","Metric Ranges"]
    sections_fieldlist = yfu.get_sectionfields()
    tab1, tab2, tab3, tab4 = st.tabs(tab_names)

    with tab1:
        tab_name = tab_names[0]
        tab_df = df[sections_fieldlist[tab_name]]
        tab_df_styled = yfu.format_dataframe(tab_df)
        st.header(tab_name)
        st.dataframe(tab_df_styled,hide_index=True)           

    with tab2:
        tab_name = tab_names[1]
        tab_df = df[sections_fieldlist[tab_name]]
        tab_df_styled = yfu.format_dataframe(tab_df)
        st.header(tab_name)
        st.dataframe(tab_df_styled,hide_index=True)
        
        # Financial charts
        fig1 = px.bar(tab_df, x='Ticker', y='trailingPE')
        st.plotly_chart(fig1)
        
        fig2 = px.bar(tab_df, x='Ticker', y='trailingEps')
        st.plotly_chart(fig2)

    with tab3:
        tab_name = tab_names[2]
        tab_df = df[sections_fieldlist[tab_name]]
        st.header(tab_name)
        st.dataframe(tab_df,hide_index=True)
        
        # Market data charts
        fig3 = px.scatter(tab_df, x='trailingPE', y='price_to_targetprice', size='pegRatio', 
                          hover_name='Ticker', title='P/E Ratio vs Payout, size is peg')
        st.plotly_chart(fig3)

    with tab4:
        tab_name = tab_names[3]
        # tab_df_styled = yfu.format_dataframe(tab_df)        
        st.header(tab_name)
        metrics = list(df.columns)[1:]

        display_metrics(metrics,df)
    

if __name__ == '__main__':
    main()