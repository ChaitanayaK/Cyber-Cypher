from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json
from scrapper import pageScrapper
load_dotenv()

class Agent:
    def __init__(self):
        self._llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        #Todo: Add role for global messages| context
        self._messages = []

    def validate(self, problem: str, solution: str):
        #Todo: Add specific aspects of business idea validation| confined
        messages = [(
            "system",
            "You are a helpful assistant that validates business ideas by returning a `list of search query(s)` that is `['query1', query2]` for google search engine through which you can give a more factual response to the user",
        ), ("human", f"Following is the problem which the user has identified:{problem} | Following is the solution that the user offers: {solution} ")]
        response = self.__respond(messages)
        response = response.replace('```json', '').replace('```', '').strip()  
        try:
            json_response = json.loads(response)
            return json_response
        except Exception as e:
            print(e)
            return None
    
    def advice(self, problem: str, solution: str, focus: str):
        messages = [(
            "system",
            f"You are strategic advisor for businesses who provides strategic advice on the focus, '{focus}'. Your response must be in depth and deep. You must think and then respond.",
        ), ("human", f"Following is the problem which the user has identified:{problem} | Following is the solution that the chatbot offers: {solution} | ")]
        response = self.__respond(messages)
        return response

    def findIndustry(self, problem: str, solution: str):
        messages = [
            (
            "system",
            f"You are a helpful assistant that returns the name of the market that corresponds most with the problem and solution. Following are the industries, you need to identify which market is most relevant and return just the name of the market",
        ),
        ("human", f"Problem: '{problem}' | Solution: '{solution}'")
        ]
        response = self.__respond(messages)
        return response
    
    def summarize(self, url: str):
        content = pageScrapper(url)
        if content:
            messages = [
                ("system",
            f"You are a excellent content parser and summarizer, your goal is to extract key insights, remove redundant details, and provide a structured summary."),
            ("human", f"Summarize this page: {content}")
            ]
            response = self.__respond(messages)
            if response:
                return response
        return "Could not summarize the page.."


    def __respond(self, messages: list):
        response = self._llm.invoke(messages)
        return response.content
