from langchain.schema import SystemMessage
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from utils.StockMarketSymbolSearchTool import StockMarketSymbolSearchTool
from utils.CompanyOverviewTool import CompanyOverviewTool
from utils.CompanyIncomeStatementTool import CompanyIncomeStatementTool
from utils.CompanyStockPerformanceTool import CompanyStockPerformanceTool
from utils.prompts.investment_main_prompt import investment_main_prompt

llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-1106")

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

        agent = initialize_agent(
            llm=llm,
            verbose=True,
            agent=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
            tools=[
                StockMarketSymbolSearchTool(),
                CompanyOverviewTool(alpha_vantage_api_key),
                CompanyIncomeStatementTool(alpha_vantage_api_key),
                CompanyStockPerformanceTool(alpha_vantage_api_key),
            ],
            agent_kwargs={
                "system_message": SystemMessage(content=investment_main_prompt)
            },
        )
        
        result = agent.invoke(query)
        st.write(result["output"].replace("$", "\$"))

    elif not openai_api_key: 
        with st.sidebar:
            url = "https://platform.openai.com/api-keys"
            error_message = f"""
                Please provide OpenAI API key to receive an investment decision.
                Create your OpenAI API key: [OpenAI]({url})
                """
            st.error(error_message)

    elif not alpha_vantage_api_key: 
        with st.sidebar:
            url = "https://www.alphavantage.co/support/#api-key"
            error_message = f"""
                Please provide Alpha Vantage API key to receive investment decision.
                Create your Alpha Vantage API key for free: [Alpha Vantage]({url})
                """
            st.error(error_message)
