from .google import GoogleAgent
from .mistral import MistralAgent 
from .openai import OpenAIAgent
from .base_code import BaseCodeAgent
from ..tools.Tool import Tool

class CodeAgent:
    """Factory class for creating AI agent instances.
    
    This class implements the factory pattern to create instances of different AI provider agents
    (Google, Mistral, etc.). It acts as a central registry for available AI providers and handles
    the instantiation of the appropriate agent class based on the provider name.

    Example:
        >>> agent = CodeAgent("google", "google-agent", tools=tools, model="gemini-2.0-flash")
        >>> response = agent("What is the capital of France?")

    Attributes:
        _providers (Dict[str, Type[BaseCodeAgent]]): Registry of available AI providers and their
            corresponding agent classes.

    Args:
        provider (str): The name of the provider to use (e.g., "google", "mistral").
        agent_name (str): The name of the agent instance.
        tools (List[Tool], optional): List of tools available to the agent. Defaults to [].
        loop_limit (int, optional): Maximum number of conversation loops. Defaults to 5.
        model (str, optional): The specific model to use with the provider. Defaults to "".

    Returns:
        BaseCodeAgent: An instance of the specified provider's agent class.

    Raises:
        ValueError: If the specified provider is not available in the registry.
    """
    # Factory class for creating code agents
    _providers: dict[str, BaseCodeAgent] = {
        "google": GoogleAgent,
        "mistral": MistralAgent,
        "openai": OpenAIAgent,
    }

    def __new__(cls, provider: str, agent_name: str, tools: list[Tool] = [], loop_limit: int = 5, model: str = ""):
        if provider.lower() not in cls._providers:
            raise ValueError(f"Unknown agent provider: {provider}.\n Available providers: {list(cls._providers.keys())}")

        provider_class = cls._providers[provider.lower()]
        instance = super().__new__(provider_class)
        if model:
            instance.__init__(agent_name=agent_name, tools=tools, loop_limit=loop_limit, model=model)
        else:
            instance.__init__(agent_name=agent_name, tools=tools, loop_limit=loop_limit)
        return instance