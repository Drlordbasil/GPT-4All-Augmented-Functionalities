# File: gpt4all_expander/submodules/business_strategy.py

from .market_analysis import MarketAnalysis

class BusinessStrategy:
    def __init__(self, model):
        self.model = model

    def generate_strategy(self, market_analysis: str) -> str:
        analysis_input = f"Market Analysis: {market_analysis}\n"
        strategy_prompt = analysis_input + "Given this analysis, devise a business strategy for a new e-commerce entrant:"
        strategy = self.model.generate(strategy_prompt, max_tokens=5000)
        return strategy