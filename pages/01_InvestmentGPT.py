from langchain.schema import SystemMessage
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from utils.StockMarketSymbolSearchTool import StockMarketSymbolSearchTool
from utils.CompanyOverviewTool import CompanyOverviewTool
from utils.CompanyIncomeStatementTool import CompanyIncomeStatementTool
from utils.CompanyStockPerformanceTool import CompanyStockPerformanceTool
from utils.prompts.investmentGPT_prompts import investment_main_prompt, InvestmentGPT_welcome_prompt

llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-1106")

st.set_page_config(
    page_title="InvestmentGPT",
    page_icon="💼",
)

st.markdown(
    InvestmentGPT_welcome_prompt,
    unsafe_allow_html=True
)

with st.sidebar:
    openai_key_exists = "openai_api_key" in st.session_state.keys()
    openai_api_key = st.text_input(
        "Enter your OpenAI API key:",
        placeholder="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        value= "" if not openai_key_exists else st.session_state["openai_api_key"]
    )

    alpha_vantage_api_key_exists = "alpha_vantage_api_key" in st.session_state.keys()
    alpha_vantage_api_key = st.text_input(
        "Enter your Alpha Vantage API key:",
        placeholder="XXXXXXXXXXXXXXXX",
        value= "" if not alpha_vantage_api_key_exists else st.session_state["alpha_vantage_api_key"]
    )


if openai_api_key:
    st.session_state["openai_api_key"] = openai_api_key

if alpha_vantage_api_key:
    st.session_state["alpha_vantage_api_key"] = alpha_vantage_api_key

# Investment info
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
                CompanyOverviewTool(alpha_vantage_api_key=alpha_vantage_api_key),
                CompanyIncomeStatementTool(alpha_vantage_api_key=alpha_vantage_api_key),
                CompanyStockPerformanceTool(alpha_vantage_api_key=alpha_vantage_api_key),
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
