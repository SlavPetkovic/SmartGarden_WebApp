import openai

openai.api_key = "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"

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, can you respond?"}],
)

print(response)  # see full response
print(response.choices[0].message["content"])  # just the text
