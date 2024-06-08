from services.voice import VoiceService
from langchain.chat_models.openai import ChatOpenAI
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory, FileChatMessageHistory
from prompts import structured_chat_prompt
from tools.internet import ExaSearchTool, TavilySearchTool
from tools.basic_tools import DateTool, TimeTool, OpenWeatherTool
from tools.vision import VisionTool, ScreenshotTool
from tools.file_selector import FileSelectorTool
from callbacks import AgentCallbacks, LLMCallbacks

vs = VoiceService()
mind = FileChatMessageHistory(file_path="data/memory.json")
memory = ConversationBufferWindowMemory(
    chat_memory=mind,
    memory_key="chat_history",
    k=20,
    return_messages=True
)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

llm = ChatOpenAI(model="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf", temperature=0, streaming=True, callbacks=[LLMCallbacks()], base_url="http://localhost:8080/v1", api_key="lm-studio")
tools = [ExaSearchTool, TavilySearchTool(), DateTool(), TimeTool(), OpenWeatherTool(), VisionTool(), ScreenshotTool(), FileSelectorTool()]

structured_chat_agent = create_structured_chat_agent(llm, tools, structured_chat_prompt)
agent = AgentExecutor(agent=structured_chat_agent, tools=tools, memory=memory, verbose=True, handle_parsing_errors="Check your output and make sure it conforms, use the Action/Action Input syntax, if it doesn't call a tool, output only the action_input.", max_iterations=2, callbacks=[AgentCallbacks()] )

#You're being opened for the first time, greet the user properly in the style of Jarvis
    
def boot(message: str = "You're being opened for the first time, Always address the user as 'Sir', and greet the user properly in the style of Jarvis"):
    try:
        response = agent.invoke({"input": message, "chat_history": memory.buffer_as_messages})
        print(f"MegaMind's Response: {response}")
        
        while True:
            text = vs.listen() or input("Enter your query here >>>> ")
            print(bcolors.BOLD+" "+bcolors.OKCYAN+ " You: "+ text)
            response = agent.invoke({"input": text, "chat_history": memory.buffer_as_messages})
            print(f"MegaMind's Response: {response}")
    except KeyboardInterrupt:
        return False
    except BaseException as e:
        boot("Your system just recovered from a crash. You encountered an error. Answer my last question, use the appropriate tools if you have to.")
    
if "__main__":
    boot()