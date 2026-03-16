from openai import OpenAI

client = OpenAI(api_key="")

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a helpful AI tutor."},
        {"role": "user", "content": "Explain what a neural network is?"},
    ],
)

print(response.choices[0].message.content)
