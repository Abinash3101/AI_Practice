# chain of thought prompting
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    #api_key="",
    #base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
    You're an expert AI Assistance in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times)
    and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

    Example:
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
"""

print("\n\n\n")

message_history = [
    {"role":"system","content": SYSTEM_PROMPT},
]

user_query = input("--> ")
message_history.append({"role":"user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type":"json_object"},
        messages=message_history
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("-->", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("...", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("<>", parsed_result.get("content"))
        break

print("\n\n\n")    