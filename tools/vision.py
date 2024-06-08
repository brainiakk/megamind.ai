import os
from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from services.webcam import capture_image
from services.voice import VoiceService
from dotenv import load_dotenv
from typing import Optional
import json
from langchain.tools import SteamshipImageGenerationTool
from langchain.schema import HumanMessage, SystemMessage
import numpy as np
from IPython.display import HTML, display
from PIL import Image
import base64
from typing import Optional, Type
from langchain_google_vertexai import ChatVertexAI
from PIL import ImageGrab
from langchain.chat_models.openai import ChatOpenAI
from tools.wrappers import internet_tool

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"


load_dotenv()
llm = ChatVertexAI(model_name="gemini-1.5-pro-001", temperature=0, streaming=True)

# llava = Ollama(model="llava", t emperature=0, system="You are an image analysis tool, you relay precise results of your analysis to the main AI called Brainiakk.")
llava = ChatOpenAI(model="llava-llama-3-8b-v1_1-int4.gguf", temperature=0, base_url=os.getenv('LMSTUDIO_API_URL'), api_key=os.getenv('LMSTUDIO_API_KEY'))

vs = VoiceService()

def encode_image(image_path):
    """Getting the base64 string"""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def plt_img_base64(img_base64):
    """Display the base64 image"""

    # Create an HTML img tag with the base64 string as the source
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'

    # Display the image by rendering the HTML
    display(HTML(image_html))

def image_model(query):
    img_path = capture_image()
    # msg = llava_process_image(img_path, query)
    msg = vertexai_process_image(img_path, query)

    print(msg)
    return msg


class VisionToolInput(BaseModel):
    img_query: str = Field(description="word it like this: 'give a detailed description of this image. Never respond in markdown format, ONLY use plain text.'")
    wait_message: str = Field(description="address the user respectfully and ask the user to hold on while you turn on the webcam and analyze the image")

class VisionTool(BaseTool):
    name="Vision Tool"
    description="Useful tool to access the user's device camera. Useful when you need to look at anything EXCEPT the user's screen or files. using the device camera and it returns the description of what's in front of the camera. Describe what you see in details. Format input: {{ 'img_query':  '...', 'wait_message': '...'}} This gives you access to vision, use it when the user tells you to take a look at anything APART from the screen or internal device files or 'what do you see', without providing proper context or image path."
    args_schema: Type[BaseModel] = VisionToolInput
    return_direct: bool = True
   
    def _run(self, img_query: str, wait_message: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        vs.piper(wait_message)
        return image_model(img_query)
 
    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("vision tool does not support async")
   

class ScreenshotInput(BaseModel):
    img_query: str = Field(..., description="Use this exact sentence here: 'give a detailed description of this image, as detailed as possible.'")
    wait_message: str = Field(..., description="you should address the user politely and ask the user to hold on while you take a screenshot of the active window.")
    
class ScreenshotTool(BaseTool):
    name="Screenshot Tool"
    description="Useful tool to take a screenshot. This tool is and only used to screenshot or look at the user's screen. **NOTE:** USE this tool ONLY when asked to look at the user's screen.  Use this tool to screenshot the user's screen. Use this tool when asked to take a screenshot. Format input: {{ 'img_query': 'give a detailed description of this image, as detailed as possible.', 'wait_message': '...' }}."
    args_schema: Type[BaseModel] = ScreenshotInput
    return_direct=True
    
    def _run(self, img_query: str, wait_message: str, run_manager: Optional[CallbackManagerForToolRun]):
        vs.piper(wait_message)
        # Capture the entire screen
        screenshot = ImageGrab.grab()
        # Save the screenshot to a file
        save_path = "data/vision/screenshot.png"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        screenshot.save(save_path)

        # Close the screenshot
        screenshot.close()
        print(save_path)
        msg = vertexai_process_image(save_path, img_query)
        print(msg)  
        return msg
        # return llava_process_image(save_path, img_query)
 
    async def _arun(
        self, img_query: str, wait_message: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await self._run(img_query, wait_message, run_manager)
    
@internet_tool
def vertexai_process_image(img, query:str):
    message = HumanMessage(
    content=[
            {
                "type": "text",
                "text": query,
            },  # You can optionally provide text parts
            {"type": "image_url", "image_url": {"url": img}},
        ]
    )
    msg = llm.invoke([message])
    
    print(msg.content)
    return msg.content

def llava_process_image(img, query):
    img_base64 = encode_image(img)
    plt_img_base64(img_base64)
    # llm_with_image_context = llava.bind(images=[img_base64])
    message = HumanMessage(
    content=[
            {
                "type": "text",
                "text": query,
            },  # You can optionally provide text parts
            {
                "type": "image_url", 
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
            },
        ]
    )
    msg = llava.invoke([message])
    
    return msg.content


# Hello Brainiakk, take a look
# Hello Brainiakk, take a look at this
# Take a look at this
# Look at these
# Hello Brainiakk, what do you see