# zero shot prompting
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# zero shot prompting: Directly giving the inst to the model
SYSTEM_PROMPT = "You should only and only ans the coding related questions. Do not answer anything else. Your name is Alexa. If somebody asks questons not related to coding just say sorry."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user", "content":"Hay, Can you write a python code to translate word hello to hindi"}
    ]
)

print(response.choices[0].message.content)
# 1. zero-shot Prompting: The model is giving a direct question or task without prior examples.