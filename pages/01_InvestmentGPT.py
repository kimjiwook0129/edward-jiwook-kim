from langchain.schema import SystemMessage
import streamlit as st
import os
import requests
from typing import Type
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.agents import initialize_agent, AgentType
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from utils.CompanyOverviewArgsSchema import CompanyOverviewArgsSchema
from utils.StockMarketSymbolSearchTool import StockMarketSymbolSearchTool
from utils.StockMarketSymbolSearchToolArgsSchema import StockMarketSymbolSearchToolArgsSchema


llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-1106")

class CompanyOverviewTool(BaseTool):
    name = "CompanyOverview"
    description = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return r.json()


class CompanyIncomeStatementTool(BaseTool):
    name = "CompanyIncomeStatement"
    description = """
    Use this to get the income statement of a company.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        income_statement = r.json()

        # Only look for most recent 3 years & 8 quarters
        income_statement['annualReports'] = income_statement['annualReports'][:3]
        income_statement['quarterlyReports'] = income_statement['quarterlyReports'][:8]

        return income_statement


class CompanyStockPerformanceTool(BaseTool):
    name = "CompanyStockPerformance"
    description = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        r = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        response = r.json()
        
        # Only look for most recent 3 years
        return list(response["Weekly Time Series"].items())[:160]   

agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    tools=[
        CompanyIncomeStatementTool(),
        CompanyStockPerformanceTool(),
        StockMarketSymbolSearchTool(),
        CompanyOverviewTool(),
    ],
    agent_kwargs={
        "system_message": SystemMessage(
            content="""
            You are a hedge fund manager.
            
            You evaluate a company and provide your opinion and reasons why the stock is a buy or not.
            
            Consider the company's income statement, stock performance, and company's overview.

            Only recommend to buy the stock if you are more than 95 percent condfident that the user will make
            their desired profit in percentage within the duration (in months) provided by the user.
            
            Provide your scores on each category: income statement, stock performance, and company's overview.

            Even if the company seems profitable, if the current stock price is too high compared to the company's value,
            and you think the user cannot make the desired profit within the given duration, then don't recommend the stock.

            Example output:
            Company: [Given company]
            Your desired profit: [given percentage] within [given_duration] months

            Company Overview ([Your score] / 5.0):

            [One or two sentences of reasoning]

            
            Income ([Your score] / 5.0):

            [One or two sentences of reasoning]

            
            Stock Performance ([Your score] / 5.0):
            
            [One or two sentences of reasoning]

            
            Your desired profit of [given percentage]% within [given_duration] months
            seems [reasonable / not reasonable].
            I would [RECOMMEND / NOT RECOMMEND] to buy [Given company] stocks at this moment.
        """
        )
    },
)

st.set_page_config(
    page_title="InvestmentGPT",
    page_icon="💼",
)

st.markdown(
    """
    # InvestmentGPT
            
    Welcome to InvestmentGPT.
            
    Write down the name of a company, your desired profit within a certain duration and our Agent will determine whether to buy the stock to satisfy your needs.

    <span style="color:red; font-weight:bold;">[Disclaimer] The results provided by this agent are for informational purposes only and may be incorrect. Investing in stocks involves risk, and it is the user's responsibility to conduct their own research and make their own investment decisions. The creators of InvestmentGPT are not liable for any financial losses that may occur.</span>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    openai_api_key = st.text_input(
        "Enter your OpenAI API key:",
        placeholder="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    )
    alpha_vantage_api_key = st.text_input(
        "Enter your Alpha Vantage API key:",
        placeholder="XXXXXXXXXXXXXXXX",
    )

company = st.text_input("Write the name of the company you are interested in.")
desired_profit = st.number_input("Enter your expected profit (%):", min_value=0.0, step=0.1)
desired_duration_in_months = st.number_input("Enter the expected duration (in months):", min_value=0.25, max_value=120.0, step=0.25)

if st.button("Submit"):
    if company and desired_profit and desired_duration_in_months and openai_api_key and alpha_vantage_api_key:
        query = {
            "input": {
                "company": company,
                "desired_profit": desired_profit,
                "desired_duration_in_months": desired_duration_in_months
            }
        }
        result = agent.invoke(query)
        st.write(result["output"].replace("$", "\$"))
    elif not openai_api_key: 
        with st.sidebar:
            # st.error("Please provide OpenAI key to receive investment decision.")
            url = "https://www.example.com"
            error_message = f"Please provide [OpenAI key]({url}) to receive an investment decision."
            st.error(error_message)

    elif not alpha_vantage_api_key: 
        with st.sidebar:
            st.error("Please provide Alpha Vantage API key to receive investment decision.")