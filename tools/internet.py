import os
from exa_py import Exa
from langchain.agents import initialize_agent, Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from typing import Optional, Type
from dotenv import load_dotenv
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
# from agents.system.tools.langchain.retriever_tools import retrieve_webpages
from tools.wrappers import internet_tool
load_dotenv()

# Set up your EXA API key
exa = Exa(os.environ.get('EXA_API_KEY'))

@internet_tool
def exa_search(input) -> str:
    """Search the web"""
    highlights_options  = {
        "num_sentences": 10, # how long our highlights should be
        "highlights_per_url": 1, # just get the best highlight for each URL
    }

    # Let the magic happen!
    info_for_llm = []
    search_response = exa.search_and_contents(input, highlights=highlights_options, num_results=5, use_autoprompt=True)
    # results = exa.get_contents([sr.id for sr in search_response.results], 
    #                         text={"include_html_tags": False, "max_characters": 1000}, 
    #                         highlights={"highlights_per_url": 2, "num_sentences": 1, "query": input})
    info = [sr.highlights[0] for sr in search_response.results]
    info_for_llm.append(info)
    # print(results.results)
    # return results.results
    print(info)
    return info

async def coroutine_exa_search(input):
    await exa_search(input)
    
ExaSearchTool = StructuredTool.from_function(
    name="ExaSearchTool",
    func=exa_search,
    description="This tool is useful to search the web. input should be the word or sentence the user want you to search for. Format input as `string`, Example: 'Who is Austin Brain'. Make sure you tell the user what URL(s) you got your answer from",
    coroutine=coroutine_exa_search
)

class DDGSearchInput(BaseModel):
    query: str = Field(description="The search query from the user")
    region: str = Field(description="The country or region from the user query example: wt-wt, us-en, uk-en, ru-ru, etc. The default is wt-wt.", default="wt-wt")
    source: str = Field(description="The search engine source to get better results for the user search query, also check in the user original search query and if none was specified, Defaults to 'text'. These are the only options allowed: 'news', 'text', 'answers', 'images', 'videos', 'maps' and 'suggestions' ", default="text")
    
class DuckDuckGoSearchTool(BaseTool):
    name="Duck Duck Go Search Tool"
    description="Useful to search the web more for better results. This is a search engine tool."
    args_schema: Type[BaseModel] = DDGSearchInput
    
    @internet_tool
    def _run(self, query: str, region: str ="wt-wt", source: str ="text", run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        wrapper = DuckDuckGoSearchAPIWrapper(region=region, max_results=5)
        search = DuckDuckGoSearchResults(api_wrapper=wrapper, source=source)
        return search.run(query)
 
    @internet_tool
    async def _arun(self, query: str, region: str ="wt-wt", source: str ="text", run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        wrapper = DuckDuckGoSearchAPIWrapper(region=region,  max_results=5)
        search = await DuckDuckGoSearchResults(api_wrapper=wrapper, source=source)
        return search.run(query)



class TavilySearchInput(BaseModel):
    query: str = Field(description="The search query to search for.")
    
class TavilySearchTool(BaseTool):
    name="Tavily Search Tool"
    description="Useful to search the web more for better results. This is a search engine tool. Format input as {{'query': 'Who is Austin Brain' }}"
    args_schema: Type[BaseModel] = TavilySearchInput
    
    @internet_tool
    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        tavily = TavilySearchResults()
        return tavily.invoke(query)
    
    @internet_tool
    async def _arun(self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        tavily = TavilySearchResults()
        return await tavily.ainvoke(query)