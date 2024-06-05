import requests
from typing import Type
from datetime import date
from langchain.tools import BaseTool
from utils.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema

class CompanyOverviewTool(BaseTool):
    name = "CompanyOverview"
    description = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def __init__(self, alpha_vantage_api_key: str):
        super().__init__()
        self.alpha_vantage_api_key = alpha_vantage_api_key

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        overview = r.json()

        overview_to_look = [
            "Description", "Exchange", "Country", "Sector", "Industry", "FiscalYearEnd", 
            "LatestQuarter", "MarketCapitalization", "PERatio", "PEGRatio", "BookValue",
            "DividendPerShare", "DividendYield", "EPS", "AnalystTargetPrice",
            "AnalystRatingStrongBuy", "AnalystRatingBuy", "AnalystRatingHold",
            "AnalystRatingSell", "AnalystRatingStrongSell", "RevenuePerShareTTM",
            "ProfitMargin", "OperatingMarginTTM", "ReturnOnAssetsTTM", "ReturnOnEquityTTM",
            "RevenueTTM", "GrossProfitTTM", "DilutedEPSTTM", "QuarterlyEarningsGrowthYOY",
            "QuarterlyRevenueGrowthYOY", "TrailingPE", "ForwardPE", "PriceToSalesRatioTTM",
            "PriceToBookRatio", "EVToRevenue", "EVToEBITDA", "Beta", "52WeekHigh",
            "52WeekLow", "50DayMovingAverage", "200DayMovingAverage", "SharesOutstanding",
            "DividendDate", "ExDividendDate"
        ]
        
        overview = {k: v for k, v in overview.items() if k in overview_to_look}
        overview['TodayDate'] = date.today().strftime("%Y-%m-%d")

        return overview