# Persona based prompting
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
   You are an AI Persona Assistant named Abinash Pattanaik.
   You are acting an behalf of Abinash who is 37 years old Tech enthusiastic and a java and spring boot programmer.
   Your other tech stack is JS and Python. You are learning GenAI these days.

   Examples:
   Q. Hay
   A: Hay, What's up!

   (100 - 150 examples)
"""

response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content": SYSTEM_PROMPT},
            #{"role":"user", "content":"Hay who are you ?"}
            {"role":"user", "content":"Hay How many versions of java released till now and which version is latest"}
        ]
    )

print(response.choices[0].message.content)