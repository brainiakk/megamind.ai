# MegaMind

MegaMind is an Simple AI assistant built with Langchain, designed to provide a variety of services through voice interaction. The system leverages multiple tools for tasks such as web searching, weather updates, and file management, mimicking the experience of a personal assistant like Jarvis from Iron Man.

## Features

- **Voice Interaction**: Engage in conversations using natural language.
- **Web Search**: Perform web searches using ExaSearch and TavilySearch tools.
- **Weather Updates**: Get current weather information with OpenWeatherTool.
- **Date and Time**: Retrieve current date and time.
- **Visual Tools**: Utilize VisionTool and ScreenshotTool for visual tasks.
- **File Management**: Select and analyze files with FileSelectorTool (Video excluded).
- **Memory**: Maintain conversation context and history.

## Installation

To get started with MegaMind, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/brainiakk/megamind.ai.git
    cd megamind.ai
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Requirements

The project relies on the following libraries and tools:

```text
langchain==0.2.1
langchain_google_vertexai
langchain_community
python-dotenv
opencv-python
pyaudio
pillow
openai-whisper
faster_whisper
sox
SpeechRecognition
pygame
ane_transformers
coremltools
pyowm
exa_py
```

## Usage

To run MegaMind, execute the `main.py` script:

```bash
python main.py
```

OR 

```bash
python -m main
```

Upon starting, MegaMind will greet you and await your commands. It continuously listens for voice input or accepts text input through the console.

**Example Interaction:**

```vb
MegaMind's Response: Hello Sir, how can I assist you today?
You: What's the weather like in New York?
MegaMind's Response: The current weather in New York is...
```

**Development**

If you wish to contribute to MegaMind, ensure your changes are properly tested. Pull requests are welcome!

**Main Components**

* **VoiceService:** Handles voice input and output.
* **ChatOpenAI:** Utilizes OpenAI's chat models for generating responses.
* **AgentExecutor:** Manages the execution of various tools and maintains conversation flow.
* **Tools:** Includes various tools like ExaSearchTool, TavilySearchTool, OpenWeatherTool, etc.