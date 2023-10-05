# File: gpt4all_expander/submodules/market_analysis.py

import yfinance as yf

class MarketAnalysis:
    def __init__(self, model):
        self.model = model

    def analyze_market_trends(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        prompt = f"Analyze the following market data for {ticker} and provide insights:\n{hist}"
        analysis = self.model.generate(prompt, max_tokens=1200)
        return analysis

    def analyze_competitor(self, ticker: str) -> str:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        prompt = f"Analyze the following competitor data for {ticker} and suggest strategic insights:\n{hist}"
        analysis = self.model.generate(prompt, max_tokens=1200)
        return analysis

    def comprehensive_analysis(self, market_ticker: str, competitor_tickers: list) -> str:
        market_analysis = self.analyze_market_trends(market_ticker)
        competitor_analyses = [self.analyze_competitor(ticker) for ticker in competitor_tickers]
        comprehensive_report = f"""
        Market Trend Analysis:
        {market_analysis}

        Competitor Analyses:
        {competitor_analyses}
        """
        return comprehensive_report