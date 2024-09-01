import unittest
from unittest.mock import patch
import pandas as pd
from yf_utils import get_tickers, get_fields, fetch_data, create_dataframe, format_dataframe, is_valid_number

class TestYahooFinanceDataFetcher(unittest.TestCase):

    def test_get_tickers(self):
        with patch('config.TICKERS', ['AAPL', 'GOOGL']):
            self.assertEqual(get_tickers(), ['AAPL', 'GOOGL'])

    def test_get_fields(self):
        with patch('config.FIELDS', ['currentPrice', 'dividendYield']):
            self.assertEqual(get_fields(), ['currentPrice', 'dividendYield'])

    @patch('yfinance.Ticker')
    def test_fetch_data(self, mock_ticker):
        mock_ticker.return_value.info = {'currentPrice': 150, 'dividendYield': 0.02}
        result = fetch_data(['AAPL'], ['currentPrice', 'dividendYield'])
        expected = [{'Ticker': 'AAPL', 'currentPrice': 150, 'dividendYield': 0.02}]
        self.assertEqual(result, expected)

    def test_create_dataframe(self):
        data = [{'Ticker': 'AAPL', 'currentPrice': 150, 'dividendYield': 0.02}]
        df = create_dataframe(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (1, 3))

    def test_is_valid_number(self):
        self.assertTrue(is_valid_number(10))
        self.assertTrue(is_valid_number(0))
        self.assertTrue(is_valid_number(3.14))
        self.assertFalse(is_valid_number('N/A'))
        self.assertFalse(is_valid_number(None))

    def test_format_dataframe(self):
        df = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'currentPrice': [150.25, 2500.75],
            'dividendYield': [0.02, 'N/A'],
            'freeCashflow': [1000000, 2000000]
        })
        pct_fields = ['dividendYield']
        large_num_fields = ['freeCashflow']
        
        styled_df = format_dataframe(df, pct_fields, large_num_fields)
        
        # Check that the result is a Styler object
        self.assertIsInstance(styled_df, pd.io.formats.style.Styler)
        
        # Check formatting of specific cells
        formatted_data = styled_df.data
        self.assertEqual(formatted_data.loc[0, 'currentPrice'], '150.25')
        self.assertEqual(formatted_data.loc[0, 'dividendYield'], '2.00%')
        self.assertEqual(formatted_data.loc[0, 'freeCashflow'], '1.00M')
        self.assertEqual(formatted_data.loc[1, 'dividendYield'], 'N/A')

if __name__ == '__main__':
    unittest.main()