import requests
from typing import Type
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
        self.alpha_vantage_api_key = alpha_vantage_api_key

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        return r.json()