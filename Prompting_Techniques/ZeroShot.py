# Zero Shot Prompting 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero shot prompting : where the model is given direct question or task without any prior example 
SYSTEM_PROMPT = "You are a math teacher, and answer doubts related to maths only. Do not answer anything apart from maths."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role" : "system", "content" : SYSTEM_PROMPT},
        {"role": "user", "content": "Hello, My name is Ankit"}
    ]
)

print(response.choices[0].message.content)