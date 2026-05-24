# Chain of thought prompting 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = '''
    You're an expert AI assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first plan what needs to be done. The PLAN can be multiple steps.
    Once you think enough plan has been done you can finally give the output.

    Rules: 
    - Strictly Follow the give JSON output format
    - Only run one step at a time
    - The sequence of steps is START(where user gives the input in string format) , then PLAN (which can be multiple steps) and then finally the OUTPUT (which is going to be displayed to the user)

    Output JSON format : 
    {"step" : "START" | "PLAN" | "OUTPUT" , "content" : "string"}

    Example : 

User: "What is 25 * 12?"

Assistant:
{"step":"START","content":"The user wants to calculate the multiplication of 25 and 12."}

Assistant:
{"step":"PLAN","content":"Multiply 25 by 12 using arithmetic calculation."}

Assistant:
{"step":"OUTPUT","content":"25 * 12 = 300"}

Example 2:

User: "Write a blog title about AI in healthcare"

Assistant:
{"step":"START","content":"The user needs a blog title related to AI in healthcare."}

Assistant:
{"step":"PLAN","content":"Generate a concise and engaging title combining AI and healthcare innovation."}

Assistant:
{"step":"PLAN","content":"It should be innovative"}

Assistant:
{"step":"OUTPUT","content":"How AI is Revolutionizing Modern Healthcare"}

'''


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role" : "system", "content" : SYSTEM_PROMPT},
        {"role": "user", "content": "Write a python code for reversing a string"}
    ]
)

print(response.choices[0].message.content)