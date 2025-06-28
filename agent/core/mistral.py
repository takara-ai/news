import os
from mistralai import Mistral
from dotenv import load_dotenv
from .prompts import load_prompt
from ..tools.Tool import Tool
from .base_code import BaseCodeAgent

# Inherit from the parent CodeAgent class for code tool calling agent functions
class  MistralAgent(BaseCodeAgent):
    def __init__(self, agent_name: str, tools: list[Tool] = [], loop_limit: int = 5, model: str = "devstral-small-latest"):
        # Inherit init
        super().__init__(agent_name, tools, loop_limit, model)
        # Set attributes
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.client = self._initialise_client()

    def __call__(self, question: str, debug: bool = False, eval_check: bool = False) -> str:
        """
        Args:
            question(str): The question for the agent to respond to 
            debug(bool, optional): If True, enables debug mode
            eval_check(bool, optional): If True, requires permission to evaluate any produced code
        """
        # Initialise chat
        self.messages.append({"role": "user", "content": question})

        # Agent loop
        for i in range(self.loop_limit):

            # Devstral response generation
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=self.messages
                )
            except Exception as e:
                return f"Mistral completion error: {e}"

            # Add agent response to messages
            self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

            # Handle debug mode
            if debug:
                # Print assistant and user messages
                print(f"-------------\nUser: {self.messages[-2]}\n-------------\nAssistant: {self.messages[-1]}\n-------------")
            
            # Check for answer
            answer = self.get_answer(response.choices[0].message.content)
            if answer: 
                return answer

            # Check for code
            code = self.get_code(response.choices[0].message.content)
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
                            self.messages.append({"role": "user", "content": "User decided not to evaluate the assistant code"})
                            continue
                        else:
                            raise Exception("Unexpected input")
                    except Exception as e:
                        print("User error: Incorrect input for eval check.")
                        return "User error: Incorrect input for eval check."

                # Evaluate code
                observation = self.eval_code(code)
                self.messages.append({"role": "user", "content": observation})
            else: 
                self.messages.append({"role": "user", "content": "Error: The assistant has not provided either an <answer> or <code> block."})

        # Handle exceeding of loop limit
        return f"No response by the loop limit: {self.loop_limit}"

    def _initialise_client(self):
        # Load mistral API key
        load_dotenv()
        key = os.getenv("MISTRAL_API_KEY")
        if not key:
            raise EnvironmentError("MISTRAL_API_KEY is not set in environment variables. Check .env")

        # Create client
        return Mistral(api_key=key)