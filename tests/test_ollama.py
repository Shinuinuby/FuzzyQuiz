
from ollama import chat

response = chat(
    model="qwen3:4b-instruct",
    messages=[
        {
            "role": "user",
            "content": "Generate one easy multiple-choice question about Python with four choices and the correct answer."
        }
    ]
)

print(response.message.content)
