import requests
from langchain.tools import BaseTool
from typing import Type
from utils.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema

class CompanyStockPerformanceTool(BaseTool):
    name = "CompanyStockPerformance"
    description = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def __init__(self, alpha_vantage_api_key: str):
        self.alpha_vantage_api_key = alpha_vantage_api_key

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        response = r.json()
        
        # Only look for most recent 3 years
        return list(response["Weekly Time Series"].items())[:160]   