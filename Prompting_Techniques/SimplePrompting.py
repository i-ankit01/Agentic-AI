from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role" : "system", "content" : "You are a math teacher, and answer doubts related to maths only. Do not answer anything apart from maths."},
        {"role": "user", "content": "Hello, My name is Ankit"}
    ]
)

print(response.choices[0].message.content)