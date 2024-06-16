import httpx
from typing import Type
from langchain.tools import BaseTool
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from utils.investmentGPT.StockMarketSymbolSearchToolArgsSchema import StockMarketSymbolSearchToolArgsSchema

class StockMarketSymbolSearchTool(BaseTool):
    name = "StockMarketSymbolSearchTool"
    description = """
    Use this tool to find the stock market symbol for a company.
    It takes a query as an argument.
    """
    args_schema: Type[
        StockMarketSymbolSearchToolArgsSchema
    ] = StockMarketSymbolSearchToolArgsSchema

    def _run(self, query):
        ddg = DuckDuckGoSearchAPIWrapper()
        try:
            return ddg.run(query)
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
            return f"HTTP error occurred: {e.response.status_code}"
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
            return f"Request error occurred: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"
    