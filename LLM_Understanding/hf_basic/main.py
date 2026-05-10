from transformers import pipeline, AutoProcessor, Gemma3ForConditionalGeneration

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it", device_map="auto")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]
print("Gemma3 supported")
pipe(text=messages)