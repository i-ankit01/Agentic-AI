# Chain of thought prompting 

from dotenv import load_dotenv
from openai import OpenAI
import json

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

print("\n\n\n")

message_history = [
    {"role" : "system", "content" : SYSTEM_PROMPT},
]

user_input = input("Ask AI >>> ")
message_history.append({"role": "user", "content": user_input},)


while True : 
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={ "type": "json_object" },
    messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role" : "assistant" , "content" : raw_result})

    parsed_result=json.loads(raw_result)

    if(parsed_result.get("step")=="START"):
        print("🔥" , parsed_result.get("content"))
        continue

    if(parsed_result.get("step")=="PLAN"):
        print("🧠" , parsed_result.get("content"))
        continue

    if(parsed_result.get("step")=="OUTPUT"):
        print("🤖" , parsed_result.get("content"))
        break

print("\n\n\n")