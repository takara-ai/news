"""
Prompt loading module

Usage:
    from prompts import load_prompt

    # Load a specific agent's system prompt
    prompt = load_prompt('test_writer')

    # Load an agent's prompt and give it access to Tool objects
    prompt = load_prompt('test_writer', [bash_tool, view_tool])

Author: Jacob Kenney
Date: 2025-05-31
Version 0.0.1
"""
import yaml
import json
from pathlib import Path
from datetime import datetime
from ..tools.Tool import Tool

def load_prompt(agent_name: str, tools: list[Tool] = [], loop_limit: int = 0):
    prompt_file = Path(__file__).parent / "prompts.yaml"
    with open(prompt_file, "r") as file:
        prompts = yaml.safe_load(file)
    try: 
        target_prompt = prompts["agents"][agent_name]["prompt"]

        # Insert current date into the prompt
        current_date = datetime.now().strftime("%Y-%m-%d")
        target_prompt = target_prompt.replace("{CURRENT_DATE}", current_date)
        
        if tools:
            for tool in tools:
                # Convert variables to suitable string representations
                inputs = {}
                for var, typeHint in tool.input.items():
                    inputs[var] = repr(typeHint)
                inputs = json.dumps(inputs)
                output = repr(tool.output)
                target_prompt += f"\nname: {tool.name}\ndescription: {tool.description}\ninput: {inputs}\noutput: {output}\n"
        else:
            # target_prompt += "The assistant does not have access to any tools on this occasion. The assistant can still use Python in <code> blocks."
            pass
        if loop_limit:
            target_prompt += f"\n---\n\n## CONDITION \n\n The assistant must provide an <answer>...</answer> with a final answer before the {loop_limit - 1}th response. The assistant will fail if an answer is not provided by the {loop_limit}th response. The assistant will provide an answer on, or before, their {loop_limit}th response."
        return target_prompt
    except KeyError:
        raise KeyError(f"Prompt not found for agent: {agent_name}")

# Example usage
if __name__ == "__main__":
    try:
        test_writer_prompt = load_prompt("content_curator")
        print(f"Loaded prompt: {test_writer_prompt}")
    except Exception as e:
        print(f"Error: {e}")