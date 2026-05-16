from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Generate a caption for this image in about 50 words",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://media.istockphoto.com/id/1171486814/photo/underwater-world-with-corals-and-tropical-fish.jpg?s=2048x2048&w=is&k=20&c=jTJZIZmlUKxUbSRlvjMhjnnHGKfAXEiHPEZry5eZkbI="
                    },
                },
            ],
        }
    ],
)

print(f"Response: {response.choices[0].message.content}")