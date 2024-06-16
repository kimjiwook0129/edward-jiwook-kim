import requests
from langchain.tools import BaseTool
from typing import Type
from pydantic import Field
from utils.investmentGPT.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema

class CompanyStockPerformanceTool(BaseTool):
    name = "CompanyStockPerformance"
    description = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema
    alpha_vantage_api_key: str = Field(..., exclude=True)

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        stockPerformance = r.json()

        stockPerformance = {
            date: {category[3:]: value for category, value in price_info.items()} for date, price_info in stockPerformance["Weekly Time Series"].items()
        }
        
        # Only look for most recent 3 years
        return list(stockPerformance.items())[:160]