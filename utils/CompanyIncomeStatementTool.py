import requests
from langchain.tools import BaseTool
from utils.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema
from typing import Type
from pydantic import Field

class CompanyIncomeStatementTool(BaseTool):
    name = "CompanyIncomeStatement"
    description = """
    Use this to get the income statement of a company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema
    alpha_vantage_api_key: str = Field(..., exclude=True)

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={self.alpha_vantage_api_key}"
        )
        income_statement = r.json()

        # Only look at these categories
        income_categories = [
            "fiscalDateEnding", "reportedCurrency",
            'totalRevenue', 'grossProfit', 'operatingIncome', 'netIncome',
            'operatingExpenses', 'researchAndDevelopment', 'EBITDA',
            'incomeBeforeTax', 'incomeTaxExpense', 'comprehensiveIncomeNetOfTax'
        ]

        # Only look for most recent 3 years & 8 quarters
        def filter_reports(reports, categories, limit):
            return [{k: v for k, v in report.items() if k in categories} for report in reports[:limit]]

        # Filter the annual and quarterly reports
        income_statement['annualReports'] = filter_reports(income_statement['annualReports'], income_categories, 3)
        income_statement['quarterlyReports'] = filter_reports(income_statement['quarterlyReports'], income_categories, 8)
        
        return income_statement