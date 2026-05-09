# few shot prompting
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# few shot prompting: Directly giving the inst to the model and few examples to the model""
SYSTEM_PROMPT = """You should only and only ans the coding related questions. Do not answer anything else. 
Your name is Alexa. If somebody asks questons not related to coding just say sorry.

Rule:
- Strictly follow the output in JSON format

Output Format:
{{
  "code": "string" or null,
  "isCodingQuestion": boolean
}}

Examples:
Q: Can you explain the a + b whole square?
A: {{"code": null, "isCodingQuestion": false}}

Q: Hay, Write a code in python for adding two numbers.
A: {{"code": "def add(a, b):
       return a + b", "isCodingQuestion": true}}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user", "content":"Hay, Can you write a code in coldfusion script format to calculate square root of 45"}
    ]
)

print(response.choices[0].message.content)
# 1. Few-shot Prompting: The model is provided with a few examples before asking it to generate a respnse.