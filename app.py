import streamlit as st
from agent import Agent
from scrapper import findMarket, getRelevantLinks

agent = Agent()

st.title("Business Starter")
st.header("Let's Validate your Idea!")

problem = st.text_area("What business category is your start up is based on and the problem you identified? (Explain in detail)")

solution = st.text_area("What is your solution to this problem? (Explain in detail)")

#-------------------------------------------

if st.button("Validate"):
    if problem and solution:
        with st.spinner("Validating your Idea..."):
            queries = agent.validate(problem=problem, solution=solution)
            # Todo: Remove below line for production
        queries = queries[:1]
        for query in queries:
            with st.spinner(f'Searching: "{query}"', show_time=True):
                results = getRelevantLinks(query)
                for result in results:
                    with st.container():
                        st.markdown(f"### [{result['title']}]({result['link']})")
                        st.write(result['snippet'])
                        title = result['title']
                        url = result['link']
                        st.markdown(f'<a href="/summary?title={title}&url={url}" target="_blank"><button>Summarize: {title}</button></a>', unsafe_allow_html=True)
                        # if st.button(f"Summarize: {result['title']}"):
                        #     with st.spinner("Validating your Idea...", show_time=True):
                        #         summary = agent.summarize(result['link'])
                        #         if summary:
                        #             js = f"window.open('/summary?title={result['title']}&url={result['link']}')"
                        #             st.markdown(f'<script>{js}</script>', unsafe_allow_html=True)

#-------------------------------------------
        st.divider()

        st.subheader("Industrial Statistics")
        with st.spinner("Identifying the corresponding industry...", show_time=True):
            industryName = agent.findIndustry(problem, solution)
            if industryName:
                industryLink = findMarket(industryName)
                if industryLink:
                    st.link_button("See Your Industry", industryLink)
    else:
        st.error("You need to explain the problem and the solution!")

#Strategic Advice Section
#-------------------------------------------
st.divider()
st.header("Get Strategic Advice")
st.write("Get AI-powered insights on execution, scaling, and growth strategies.")

# Dropdown for selecting strategic focus
advice_type = st.selectbox("What kind of advice do you need?", [
    "Market Entry Strategy",
    "Scaling & Growth",
    "Revenue & Monetization",
    "Competitive Positioning",
    "Investor Pitch & Fundraising"
])

# Advice Button
if st.button("Get Strategic Advice"):
    if problem and solution:
        with st.spinner(f"Generating strategic advice on {advice_type}...", show_time=True):
            advice_response = agent.advice(problem=problem, solution=solution, focus=advice_type)
        if advice_response:
            st.subheader(f"Strategic Advice: {advice_type}")
            st.write(advice_response)
    else:
        st.error("Please provide your problem and solution first!")
pass

# # Sidebar
# st.sidebar.header("Sidebar Menu")
# option = st.sidebar.selectbox("Choose an option:", ["Home", "About", "Contact"])
# st.sidebar.write(f"You selected: {option}")
