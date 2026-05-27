import tiktoken

# Load GPT-4's tokenizer
enc = tiktoken.get_encoding("cl100k_base")

# The exact prompt from your script
prompt = "Write a poem about silicon."
print(f"Full prompt IDs: {enc.encode(prompt)}")

# Verifying your specific script claims
print(f"'silicon' ID: {enc.encode('silicon')}")
print(f"' silicon' ID: {enc.encode(' silicon')}")
print(f"' photolithography' IDs: {enc.encode(' photolithography')}")
print(f"' photo' ID: {enc.encode(' photo')}")
print(f"'lith' ID: {enc.encode('lith')}")
print(f"'ography' ID: {enc.encode('ography')}")