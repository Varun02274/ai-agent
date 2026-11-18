import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, functions

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = (
    Path(__file__).parent.parent / "prompts"/ "puzzle.md"
).read_text(encoding="utf-8")



messages = [{"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":"begin"}]

while True:

    response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    tools=tools,
)

    message = response.choices[0].message

    messages.append(message)

    if message.tool_calls:

        for tool_call in message.tool_calls:

            args = json.loads(tool_call.function.arguments)

            result = functions[tool_call.function.name](**args)

            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content": json.dumps(result)
            })

    else:

        print(message.content)

        break




