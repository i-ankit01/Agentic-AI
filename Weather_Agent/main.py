import json
import requests
from dotenv import load_dotenv
# from langfuse.decorators import observe
# from langfuse.openai import openai
import os
from openai import OpenAI


# from langsmith import traceable
load_dotenv()

# client = wrap_openai(OpenAI())
client = OpenAI()

def get_weather(city: str):
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"


def add(x, y):
    print("🔨 Tool Called: add", x, y)
    return x + y

avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "add": {
        "fn": add,
        "description": "Takes two numbers as input and returns the sum of it."
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation step and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "tool": "The name of tool if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - add: Takes two numbers as input and returns the sum of it.
    
    Example:
    User Query: What is the weather of delhi?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of delhi" }}
    Output: {{ "step": "plan", "content": "let me check the available tools to see if i can find one" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "tool": "get_weather", "input": "delhi" }}
    Output: {{ "step": "observe", "output": "The weather at delhi is 30 C" }}
    Output: {{ "step": "output", "content": "The weather for delhi seems to be 30 degrees." }}
"""

messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('Ask AI >> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("tool")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                output = avaiable_tools[tool_name].get("fn")(tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue
        
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break


    


