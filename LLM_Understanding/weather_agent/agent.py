from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
import subprocess
import platform

load_dotenv()

client = OpenAI(
    #api_key="",
    #base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd: str):
    """
    Run shell commands on both Windows and Unix systems.
    """

    is_windows = platform.system() == "Windows"

    if is_windows:
        # Use PowerShell on Windows
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
    else:
        # Use bash on Linux/macOS
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    return {
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    }



def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%c+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = """
    You're an expert AI Assistance in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the listof available tools.
    For every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times)
    and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string","tool":"string","input":"string"}

    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city.
    - run_command(cmd: str): Takes a system linux command as string and execute the command on user's system and returns the output from that command.


    Example 1:
    START: Hay can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in math problems"}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve it using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is  correct thing to apply here"}
    PLAN: {"step": "PLAN", "content": "First we must multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "Now we must perform the division that is 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now finally let's perform the addition which is 2 + 1.5 = 3.5"}
    PLAN: {"step": "PLAN", "content": "Great, we have solved the question and finaly the answer is 3.5"}
    OUTPUT: {"step": "OUTPUT", "content": "3.5"}

    Example 2:
    START: What is the weather of Delhi ?
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in getting weather of Delhi in India"}
    PLAN: {"step": "PLAN", "content": "Lets see if we have any available tool fromm the list of available tools"}
    PLAN: {"step": "PLAN", "content": "Great, we have get_weather tool available for this query."}
    PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for delhi as input city"}
    PLAN: {"step": "TOOL", "tool":"get_weather", "input": "delhi"}
    PLAN: {"step": "OBSERVE", "tool":"get_weather", "output": "The weather in delhi is ☀️  +35°C"}
    PLAN: {"step": "PLAN", "content": "Great, I got the weather info about delhi"}
    OUTPUT: {"step": "OUTPUT", "content": "The temp in delhi is bright sunny and +35°C"}
"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input: Optional[str] = Field(None, description="The input params for the tool")

message_history = [
    {"role":"system","content": SYSTEM_PROMPT},
]

while True:
    user_query = input("--> ")
    message_history.append({"role":"user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model="gpt-5-nano",
            response_format=MyOutputFormat,
            messages=message_history
        )
        parsed_result = response.choices[0].message.parsed
        message_history.append({"role": "assistant", "content": parsed_result.model_dump_json()})

        if parsed_result.step == "START":
            print("-->", parsed_result.content)
            continue

        if parsed_result.step == "PLAN":
            print("...", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"~: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"~: {tool_to_call} ({tool_input}) = {tool_response}")
            message_history.append({"role": "developer", "content": json.dumps(
                {"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
            )})
            continue

        if parsed_result.step == "OUTPUT":
            print("<>", parsed_result.content)
            break

    print("\n\n\n")    