from transformers import AutoProcessor

processor = AutoProcessor.from_pretrained(
    "google/gemma-3-4b-it",
    trust_remote_code=True,
    force_download=True
)

print("processor loaded")