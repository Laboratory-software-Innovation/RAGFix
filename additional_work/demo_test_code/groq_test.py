import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # This line brings all environment variables from .env into os.environ

print(os.environ.get("GROQ_API_KEY"))
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)



chat_completion = client.chat.completions.create(
    messages=[
        # Example user prompt
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        },
        # Example system prompt
        {
            "role": "system",
            "content":
            "You are a helpful assistant. You reply with very short answers."
        }
    ],
    model="llama3-8b-8192",
    # Example Temperature
    temperature=0.5
)

# Models I can use
# llama3-8b-8192
# llama3-70b-8192
# mixtral-8x7b-32768
# gemma-7b-it
# gemma2-9b-it

print(chat_completion.choices[0].message.content)