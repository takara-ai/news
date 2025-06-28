import os
from google import genai
from google.genai import types
from google.genai.types import Content
from dotenv import load_dotenv
from .prompts import load_prompt
from ..tools.Tool import Tool
from .base_code import BaseCodeAgent

class GoogleAgent(BaseCodeAgent):
    def __init__(self, agent_name: str, tools: list[Tool] = [], loop_limit: int = 5, model: str = "gemini-2.0-flash"):        
        # Inherit init
        super().__init__(agent_name, tools, loop_limit, model)
        # Set attributes
        self.messages = []
        self.client = self._initialise_client()

    def __call__(self, question: str, debug: bool = False, eval_check: bool = False) -> str:
        """
        Args:
            question(str): The question for the agent to respond to 
            debug(bool, optional): If True, enables debug mode
            eval_check(bool, optional): If True, requires permission to evaluate any produced code
        """
        # Initialise chat
        self.messages.append({"role": "user", "parts": [{"text": question}]})

        # Agent loop
        for i in range(self.loop_limit):
            # Google response generation
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_prompt,
                        temperature=0.7
                    ),
                    # contents=[f"#{message["role"]}\n{message["content"]}" for message in self.messages],
                    contents=[f"{message["parts"][0]["text"]}" for message in self.messages]
                    # contents=self.messages
                )
            except Exception as e:
                return f"Google, {self.model} completion error: {e}"
            
            # Add agent response to messages
            self.messages.append({"role": "model", "parts": [{"text": response.text}]})

            # Handle debug mode
            if debug:
                # Print assistant and user messages
                print(f"-------------\nUser: {self.messages[-2]}\n-------------\nAssistant: {self.messages[-1]}\n-------------")

            # Check for code
            code = self.get_code(response.text)
            # Check for answer
            answer = self.get_answer(response.text)
            # Evaluate response
            if code:
                # Handle eval check protection
                if eval_check:
                    try:
                        print(f"Code to evaluate:\n\n{code}")
                        evaluate = int(input("\n0: Do not evaluate code and cull agent\n1: Evaluate code\n2: Do not evaluate code and inform agent\nDecision:"))
                        if evaluate == 0:
                            return "Agent process ended by user at eval check"
                        elif evaluate == 1:
                            pass
                        elif evaluate == 2:
                            print("Code not evaluated, agent informed")
                            self.messages.append({"role": "user", "parts": [{"text": "User decided not to evaluate assistant code"}]})
                            continue
                        else:
                            raise Exception("Unexpected input")
                    except Exception as e:
                        print("User error: Incorrect input for eval check.")
                        return "User error: Incorrect input for eval check."

                # Evaluate code
                observation = self.eval_code(code)
                self.messages.append({"role": "user", "parts": [{"text": f"Observation: {observation}"}]})
            elif answer:
                return answer
            else: 
                self.messages.append({"role": "user", "parts": [{"Text": "Error: The assistant has not provided either an <answer> or <code> block."}]})

        # Handle exceeding of loop limit
        return f"No response by the loop limit: {self.loop_limit}"

    def _initialise_client(self):
        # Load google API key
        load_dotenv()
        key = os.getenv("GOOGLE_API_KEY")
        if not key:
            raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables. Check .env")

        # Create client
        return genai.Client(api_key=key)