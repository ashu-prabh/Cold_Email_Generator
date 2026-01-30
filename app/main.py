try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
        
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Friendly", "Persuasive", "Witty"], index=0)
        
    with col3:
        cta = st.text_input("Call to Action", value="Book a meeting")

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                portfolio_links = portfolio.query_links(skills)
                
                # Industry specific links
                industry = llm.identify_industry(job.get('description', ''))
                industry_links = portfolio.query_industry_links(industry)
                
                links = portfolio_links + industry_links
                
                email = llm.write_mail(job, links, tone, cta)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


