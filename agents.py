from langchain.agents import create_agent
#from langchain_openai import ChatOpenAI
#from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

#model setup 
#llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-lite",temperature=0, api_key=st.secrets["GEMINI_API_KEY"])
api_key = st.secrets["GEMINI_API_KEY"]

# Primary model
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=api_key,
    max_retries=2,
    timeout=60,
)

# Alternative fallback model (lite / pro models typically run on separate queues)
fallback_llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite", google_api_key=api_key, max_retries=2
)

# Use this combined 'llm' in create_agent(...)
llm = primary_llm.with_fallbacks([fallback_llm])

#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
