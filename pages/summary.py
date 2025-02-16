import streamlit as st
from urllib.parse import urlparse, parse_qs
from agent import Agent

agent = Agent()

st.title("Summarizer")

query_params = st.query_params
title = query_params.get("title", [""])
url = query_params.get("url", [""])

st.header(title)

with st.spinner(f"Summarizing: {title}", show_time=True):
    content = agent.summarize(url)
    st.write(content)

# st.write(f"The URL passed from the first page: {url}")
