from typing import Dict, List
import  json


class TickerData:
    def __init__(self, ticker: str, update_cache = False) -> None:
        ticker = ticker.upper()
        self.fetch_ticker(ticker, update_cache)

    def fetch_ticker(self, ticker: str, update_cache: bool):
        cache = f'./data/{ticker}.json'
        if update_cache:
            from yahooquery import Ticker as YTicker
            yticker = YTicker(ticker)
            raw_balance_sheet = yticker.balance_sheet().transpose()
            renamed = raw_balance_sheet.set_axis(list(range(len(raw_balance_sheet.columns))), axis=1)
            balance_sheet = json.loads(renamed.to_json())

            import yfinance as yf
            ticker = yf.Ticker(ticker)
            info = ticker.get_info()
            news = ticker.news
            price_sixm = json.loads(ticker.history('6mo').to_json()) 
            price_threey = json.loads(ticker.history('3y').to_json())
            with open(cache, 'w') as f:
                json.dump({'info': info, 'news': news, 'price_sixm':price_sixm,'price_threey':price_threey, 'balance_sheet':balance_sheet }, f)


        with open(cache, 'r') as f:
            cached_data = json.load(f)
            self.info = cached_data['info']
            self.news = cached_data['news']
            self.price_sixm = cached_data['price_sixm']
            self.price_threey = cached_data['price_threey']
            self.balance_sheet = cached_data['balance_sheet']

    @property
    def financial_info(self) -> List[Dict]:
        data = [
            {'title': 'Market cap', 'value': self.info['marketCap']},
            {'title': 'PE Ratio', 'value': self.info['forwardPE']},
            {'title': 'Total revenue', 'value': self.info['totalRevenue']},
            {'title': 'Gross profit', 'value': self.info['grossProfits']},
            {'title': 'Debt to equity', 'value': self.info['debtToEquity']},
            {'title': 'Profit margin', 'value': self.info['profitMargins']},
        ]
        return data

    # @property
    # def analysis(self):
    #     return self._ticker.analysis.transpose()
