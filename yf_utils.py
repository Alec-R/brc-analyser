import yfinance as yf
import pandas as pd
import yf_config
from yf_config import DEFAULT_BARRIER, DEFAULT_COUPON


class DataHandler():
    """ 
    Handles yahoo finance data calls and transforms
    """
    df: pd.DataFrame

    def __init__(self) -> None:
        self.df = pd.DataFrame(fetch_data(get_tickers(),get_fields()))
        self.df_calculations()

    def df_calculations(self, input_barrier:float = DEFAULT_BARRIER , input_coupon = DEFAULT_COUPON) -> pd.DataFrame:
        coupon = input_coupon/100
        barrier = input_barrier/100
        # creates a dict with all the tickers for the manual EPS input 

        # inputs
        # df.join(input_eps,on='Ticker')
        self.df['eps_projected_manual'] = 1

        ## calculations
        # recalculate the price to earnings to check
        self.df['trailing_calc_pe_check'] = ( (self.df['currentPrice'] / self.df['trailingEps']) != self.df['trailingPE'] )
        # projected eps growth
        self.df['projected_eps_growth'] = (self.df['forwardEps'] / self.df['trailingEps']  - 1 )
        # the price at barrier level
        self.df['price_exbarrier'] = self.df['currentPrice'] * barrier
        # the new PE if the price is at barrier level
        self.df['drawdown_pe'] = self.df['price_exbarrier'] / self.df['trailingEps']
        # the new projected PE if the price is at barrier level - consensus eps projection from yfinance 
        self.df['drawdown_pe_projected'] = self.df['price_exbarrier'] / self.df['forwardEps']
        # the new projected PE if the price is at barrier level - manual eps input
        self.df['drawdown_pe_projected_manual'] = self.df['price_exbarrier'] / self.df['eps_projected_manual']
        # price to mean target percentage diff
        self.df['price_to_targetprice'] = ( self.df['targetMeanPrice'] / self.df['currentPrice'] ) - 1

        return self.df

        

# ==================
# handle config 
# ==================
def is_valid_number(x) -> bool :
    """Check if x is a number (not 'N/A' or None)."""
    return x != 'N/A' and x is not None

def get_tickers() -> list :
    """Read tickers from config file."""
    return yf_config.SAMPLE_TICKERS

def get_fields() -> list :
    """Read fields from config file."""
    return yf_config.FIELDS

def get_pct_fields() -> list :
    """Read fields from config file."""
    return yf_config.PCT_FIELDS

def get_largenum_fields() -> list :
    """Read fields from config file."""
    return yf_config.LARGE_INTS

def get_sectionfields() -> dict:
    """
    Supported tabs:
    "Overview", "Fundamentals", "Forward View"
    """
    basics = yf_config.basics
    overview = basics + yf_config.basics_comparison + yf_config.stock_data 
    fundamentals = basics + yf_config.financials
    forward_view = basics + yf_config.fwd_data
    
    fieldlist = {
        "Overview": overview,
        "Fundamentals": fundamentals,
        "Forward View": forward_view
    }
    return fieldlist

# ==================
# data
# ==================
def fetch_data(tickers, fields) -> list[dict] :
    """Fetch data for given tickers and fields."""
    data = []
        
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        row = {'Ticker': ticker}
        for field in fields:
            row[field] = stock_info.get(field, 'N/A')
        data.append(row)
    return data


def export_to_excel(df, filename='stock_data.xlsx') -> None:
    """Export DataFrame to Excel file."""
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")

# ==================
# view 
# ==================

def format_dataframe(df, pct_fields=get_pct_fields(), large_num_fields=get_largenum_fields()):
    """
    Format DataFrame using Pandas styling.
    
    :param df: DataFrame to format
    :param pct_fields: List of fields to format as percentages
    :param large_num_fields: List of fields to format in millions with 'M' suffix
    """
    # Convert numeric columns to float
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].astype(float)
    
    # Prepare formatting dict
    format_dict = {}
    
    # Format percentage fields
    for col in pct_fields:
        if col in df.columns:
            format_dict[col] = lambda x: f'{float(x):,.2%}' if is_valid_number(x) else 'N/A'
    
    # Format large number fields
    for col in large_num_fields:
        if col in df.columns:
            format_dict[col] = lambda x: f'{float(x)/1e6:,.2f}M' if is_valid_number(x) else 'N/A'
    
    # Format remaining numeric fields with thousands separator and 2 decimal places
    for col in numeric_columns:
        if col not in format_dict and col != 'Ticker':
            format_dict[col] = lambda x: f'{float(x):,.2f}' if is_valid_number(x) else 'N/A'
    
    # Apply the formatting
    styled_df = df.style.format(format_dict)
    
    # Add more styling
    styled_df = styled_df.set_properties(**{'text-align': 'right'})
    styled_df = styled_df.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': '.col0', 'props': [('text-align', 'left')]}  # Align Ticker column to left
    ])
    
    return styled_df