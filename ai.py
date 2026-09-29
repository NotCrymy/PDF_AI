from ollama import chat

response = chat(
    model="lfm2.5-local",
    messages=[
        {
            "role": "user",
            "content": "Bonjour, présente-toi."
        }
    ]
)

print(response.message.content)