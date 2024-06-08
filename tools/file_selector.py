import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import re
from rich.console import Console
from rich.panel import Panel
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type, Dict, List, Optional
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from unstructured.file_utils.file_conversion import convert_file_to_text
from unstructured.partition.auto import partition

# from modules import editor
from services.voice import VoiceService
from tools.vision import vertexai_process_image, llava_process_image
import soundfile
from pydub import AudioSegment
vs = VoiceService()

def open_file() -> str:
    """Opens a file selection dialog and returns the selected file path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfile()
    if not file_path:
        return None
    root.destroy()
    return file_path.name



class FileSelectorInput(BaseModel):
    message: str = Field(description="address the user respectfully and ask the user to select the file that needs to be analyzed.")
    file_type: str = Field(description="The file type the user told you needed analyzing, from the user query. If none was provided then set this to 'none', if a file type was provided set it to any of these that it is categorized under: 'audio', 'video', 'image' and 'text'. Example: If the user said to analyze music or mp3 then set it to 'audio'. Any of these are the only allowed values 'none', 'audio', 'video', 'image', 'text'")
    
class FileSelectorTool(BaseTool):
    name = "FileSelectorTool"
    description = """
    \n Useful tool to select a file accepted file types are `audio`, `video`, `image` and `text`.
    \n The accepted file types are `audio`, `video`, `image` and `text`.
    \n Useful tool when you need the user to select a file to analyse or take a look at.
    \nUse this tool if the user wants you to analyze a file and no file path is specified.
    \nUseful tool to request a file to be selected by the user.
    \n Format exactly: {{\"message\": \"address the user respectfully and ask the user to select the file that needs to be analyzed.\", \"file_type\": \"The file type the user told you needed analyzing, from the user query. If none was provided then set this to 'none', if a file type was provided set it to any of these that it is categorized under: 'audio', 'video', 'image' and 'text'. Example: If the user said to analyze music or mp3 then set it to 'audio'. Any of these are the only allowed values 'none', 'audio', 'video', 'image', 'text'\"}}                   
    """
    args_schema: Type[BaseModel] = FileSelectorInput
    return_direct=True

    def _run(self, message: str, file_type: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        Useful tool to select a file accepted file types are `audio`, `video`, `image` and `text`.

        Parameters:
        - message: address the user respectfully and ask the user to select the file that needs to be analyzed.
        - file_type: The file type the user told you needed analyzing, from the user query. If none was provided then set this to 'none', if a file type was provided set it to any of these that it is categorized under: 'audio', 'video', 'image' and 'text'. Example: If the user said to analyze music or mp3 then set it to 'audio'. Any of these are the only allowed values 'none', 'audio', 'video', 'image', 'text'
        
        Returns:
        - A string describing the file contents and the file type
        """
        try:
            vs.piper(str(message))
            selected_file, result = self.open_file(file_type)
            return f"According to my analysis, the file: {os.path.basename(selected_file)}. Contains: {result}."
        except Exception as e:
            return f"An error occurred: {e}"

    async def _arun(self, message: str, file_type: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """
        Useful tool to select a file accepted file types are `audio`, `video`, `image` and `text`.

        Parameters:
        - message: address the user respectfully and ask the user to select the file that needs to be analyzed.
        - file_type: The file type the user told you needed analyzing, from the user query. If none was provided then set this to 'none', if a file type was provided set it to any of these that it is categorized under: 'audio', 'video', 'image' and 'text'. Example: If the user said to analyze music or mp3 then set it to 'audio'. Any of these are the only allowed values 'none', 'audio', 'video', 'image', 'text'
        
        Returns:
        - A string describing the file contents and the file type
        """
        try:
            return await self._run(message, file_type, run_manager)
        except Exception as e:
            return f"An error occurred: {e}"
        
    
    def open_file(self, file_type: str = 'none') -> str:
            """Opens a file selection dialog and returns the selected file path."""
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.askopenfile(title="Select a file", initialdir=os.getcwd(), filetypes=[("All files", "*.*")])

            if not file_path:
                return None
            root.destroy()
            file_path = file_path.name

            result = self.handle_file(file_path, file_type)
            return file_path, result

    def handle_file(self, file_path: str, file_type: str = None) -> str:
        """Detects the file type based on the file extension."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext in ['.txt', '.doc', '.docx', '.pdf', '.md'] or file_type == 'text':
            print("📄 Document selected:", ext)
            elements = partition(file_path)
            return str("\n\n".join([str(el) for el in elements]))
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'] or file_type == 'image':
            print("🌆 Image selected:", ext)
            return vertexai_process_image(file_path, 'give a detailed description of this image')
        # elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'] or file_type == 'video':
        #     print("🎬 Video selected:", ext)
        #     print("Can't handle video files")
        #     return "Can't handle video files"
        elif ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg'] or file_type == 'audio':
            print("🔉 Audio selected:", ext)
            file = "outputs/analyzed_audio.wav"
            sound = AudioSegment.from_file(file_path)
            sound.set_channels(1)
            sound = sound.set_frame_rate(16000)                
            # sound = sound.set_channels(1)    
            sound.export(file, format="wav", bitrate=16000)
            
            return vs.process_audio(file)
        else:
            print("Unsupported file type")
            return "Unsupported file type"

