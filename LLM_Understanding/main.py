import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hay There! My name is Abinash Pattanaik"
tokens = enc.encode(text)

# Tokens  [49831, 3274, 0, 3673, 1308, 382, 3483, 258, 1229, 111346, 1480, 507]
print("Tokens ", tokens)

decoded = enc.decode([49831, 3274, 0, 3673, 1308, 382, 3483, 258, 1229, 111346, 1480, 507])
print("Decoded ", decoded)