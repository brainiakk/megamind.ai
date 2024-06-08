from datetime import datetime
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from typing import Optional, Type
from langchain_community.utilities import OpenWeatherMapAPIWrapper

os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPEN_WEATHER_API_KEY")


weather = OpenWeatherMapAPIWrapper()

class DateTool(BaseTool):
    name = "DateTool"
    description = "Useful tool to check the current date."
    alias="is_single_input"
    return_direct=True
    
    def _run(self, input: str = 'None', run_manager: Optional[CallbackManagerForToolRun] = None):
        date = "The date is "+ datetime.today().strftime("%A, %B %d %Y")
        print(date)
        return date
    
    async def _arun(self, input: str = 'None', run_manager: Optional[CallbackManagerForToolRun] = None):
        return await self._run(input, run_manager)

class TimeTool(BaseTool):
    name = "TimeTool"
    description = "Useful tool to check the time."
    alias="is_single_input"
    return_direct=True
    
    def _run(self, input: str = 'None', run_manager: Optional[CallbackManagerForToolRun] = None):
        time = "The time is "+ datetime.today().strftime("%H:%M %p")
        print(time)
        return time
    
    async def _arun(self, input: str = 'None', run_manager: Optional[CallbackManagerForToolRun] = None):
        return await self._run(input, run_manager)
    
class WeatherInput(BaseModel):
    location: str = Field(description="Format input as: {{ 'location': 'Location provided by the user, if none provided set this value to Lagos' }}")    
class OpenWeatherTool(BaseTool):
    name = "OpenWeatherTool"
    description="Use this tool to check the weather. Format input as: {{ 'location': 'Location provided by the user, if none provided set this value to Lagos' }}"
    alias='is_single_input'
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, location: str = 'Lagos', run_manager: Optional[CallbackManagerForToolRun] = None):
        return weather.run(location)
    
    async def _arun(
        self, location: str = 'Lagos', run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await self._run(location, run_manager)