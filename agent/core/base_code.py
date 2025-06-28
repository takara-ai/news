import re
import io
import contextlib
from abc import ABC, abstractmethod
from .prompts import load_prompt
from ..tools.Tool import Tool

class BaseCodeAgent(ABC):
    # Abstract base class for code agents
    
    def __init__(self, agent_name: str, tools: list[Tool] = [], loop_limit: int = 5, model: str = ""):
        # Load system prompt
        self.tools = tools
        self.loop_limit = loop_limit
        self.model = model
        self.system_prompt = load_prompt(agent_name, self.tools, self.loop_limit)
        
    @abstractmethod
    def _initialise_client(self):
        # Initialise the client
        pass

    @abstractmethod
    def __call__(self, question: str, debug: bool = False, eval_check: bool = False) -> str:
        # Process a question and return an answer
        pass

    def get_answer(self, message: str) -> str | None:
        # Extract the <answer>...</answer> inside a message, or None
        return self._regex_match(message, r"<answer>(.*?)</answer>")

    def get_code(self, message: str) -> str | None:
        # Extract the <code>...</code> inside a message, or None
        message = self._replace_markdown_code(message)
        return self._regex_match(message, r"<code>(.*?)</code>")

    def eval_code(self, code: str) -> str:
        # Interpret Python and return its output, or "(No output)"
        buffer = io.StringIO()
        local_vars = {tool.name: tool for tool in self.tools}
        try:
            with contextlib.redirect_stdout(buffer):
                exec(code, {}, local_vars)
            return buffer.getvalue().strip() or "(No output)"
        except Exception as e:
            return f"[Execution error] {str(e)}"

    def _regex_match(self, message: str, regexp: str) -> str | None:
        # Helper for regex matching
        match = re.search(regexp, message, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _replace_markdown_code(self, text: str):
        # Helper for replacing markdown code specification
        pattern = re.compile(r"```python\s*([\s\S]*?)```", re.MULTILINE)
        return pattern.sub(lambda m: f"<code>{m.group(1).rstrip()}</code>", text)
