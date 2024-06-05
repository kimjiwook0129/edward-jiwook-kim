import requests
from langchain.tools import BaseTool
from utils.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema
from typing import Type

class CompanyIncomeStatementTool(BaseTool):
    name = "CompanyIncomeStatement"
    description = """
    Use this to get the income statement of a company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def __init__(self, alpha_vantage_api_key: str):
        self.alpha_vantage_api_key = alpha_vantage_api_key

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        income_statement = r.json()

        # Only look for most recent 3 years & 8 quarters
        income_statement['annualReports'] = income_statement['annualReports'][:3]
        income_statement['quarterlyReports'] = income_statement['quarterlyReports'][:8]

        return income_statement