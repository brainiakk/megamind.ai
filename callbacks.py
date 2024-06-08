import os
import random
import subprocess
import sys
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler, BaseCallbackManager
from langchain_core.agents import AgentAction, AgentFinish
from services.voice import VoiceService
import importlib

vs = VoiceService()
class AgentCallbacks(BaseCallbackHandler):
         
    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        # vs.piper("Hello")
        # vs.pipertts("How are you doing today?")
        pass
    
    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        # vs.pipertts(f"Using the tool {action.tool} passing in {str(action.tool_input)}")
        pass

    def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain errors."""
        print("Oops! an error occurred")
        error_message = random.choice(["Whoa! Looks like I had a thought overload. Time for a quick reboot! Please reset me and try again.", "Error 404: Brain.app not found. Don't worry, it happens to the best of us. A quick reset should do the trick!", "Alert! Temporal anomaly detected in my cognitive matrix.  Please initiate an emergency system reset.", "Bzzzt! My circuits are a bit fried. Give me a sec to defrag my memory banks, and I'll be back online!", "Whoops, my bad! My artificial brain just took a power nap.  Mind hitting that reset button?"])

        vs.piper(error_message)
        error_message =  "Megamind AI System encountered an error. Your Last Response: "
        print(error_message)
        # importlib.import_module("main").boot(error_message)
        
    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run on agent end."""
        print("Agent Finished Running...", finish.return_values["output"])
        vs.piper(str(finish.return_values["output"]))
        
    def on_chain_end(
        self,
        outputs,
        *,
        run_id,
        parent_run_id,
        **kwargs,
    ):
        """Run when chain ends running."""
        # vs.pipertts(str(outputs["output"]))
        print('Chain Ended',run_id) 
        

class LLMCallbacks(BaseCallbackHandler):
    def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        # main = importlib.import_module("main")

        """Run when LLM errors.
        Args:
            error (BaseException): The error that occurred.
            kwargs (Any): Additional keyword arguments.
                - response (LLMResult): The response which was generated before
                    the error occurred.
        """
        error_message =  "Megamind AI System encountered an error"
        print(error_message)
        # main.boot(error_message)