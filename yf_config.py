# List of stock tickers
SAMPLE_TICKERS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# List of fields to fetch from Yahoo Finance
FIELDS = [
    'currentPrice', # last price
    'trailingPE', # Price to earnings ratio
    'trailingEps', # current earnings per share
    'forwardEps', # projected earnings per share
    'pegRatio' # pe growth using pe and eps

    'dividendYield', # dividend yield
    'targetMeanPrice', # target price consensus

    'profitMargins', # profit margin
    'operatingMargins', # operating margin

    'returnOnEquity', # return on equity
    'returnOnAssets', # return on assets
        
    'priceToBook', # price to book ratio
    'freeCashflow', # free cash flow amount
    'earningsQuarterlyGrowth', # earnings: beat/miss
    'shortRatio', # short ratio
    'payoutRatio', # Dividend payout ratio
    'beta' # beta
]

PCT_FIELDS = [
    ## yf called
    'dividendYield', # dividend yield
    'profitMargins', # profit margin
    'operatingMargins', # operating margin
    'returnOnEquity', # return on equity
    'returnOnAssets', # return on assets
    'earningsQuarterlyGrowth', # earnings: beat/miss
    'payoutRatio' # Dividend payout ratio

    ## calculated
    # ...
]

LARGE_INTS = [
    'freeCashflow', # free cash flow amount
]


basics = [
    'currentPrice', # last price
    'trailingPE', # Price to earnings ratio
    'trailingEps', # current earnings per share
    'pegRatio' # pe growth using pe and eps
]

basics_comparison =[
    'price_exbarrier', # the price at barrier level
    'drawdown_pe', # the new PE if the price is at barrier level
    'drawdown_pe_projected', # the new projected PE if the price is at barrier level - consensus eps projection from yfinance 
    'drawdown_pe_projected_manual', # the new projected PE if the price is at barrier level - manual eps input
]

fwd_data = [
    'earningsQuarterlyGrowth', # earnings: beat/miss
    'forwardEps', # projected earnings per share
    'targetMeanPrice', # target price consensus
    'pegRatio', # pe growth using pe and eps
    'projected_eps_growth' # projected eps growth
    'price_to_targetprice'
]

stock_data = [
    'shortRatio', # short ratio
    'beta' # beta
]

financials = [
    'dividendYield', # dividend yield

    'profitMargins', # profit margin
    'operatingMargins', # operating margin

    'returnOnEquity', # return on equity
    'returnOnAssets', # return on assets
        
    'priceToBook', # price to book ratio
    'freeCashflow', # free cash flow amount  
    'payoutRatio', # Dividend payout ratio
]