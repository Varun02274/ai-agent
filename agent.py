import os
import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from tools import tools, functions

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = (
    Path(__file__).parent / "system.md"
).read_text(encoding="utf-8")

iterations = 1

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT,
    },
    {"role": "user", "content": f"iteration: {iterations}"}
]

BOLD_CYAN = "\033[1;96m"
RESET = "\033[0m"

print(f"\n{BOLD_CYAN}{'=' * 40}")
print(f"  ITERATION {iterations}")
print(f"{'=' * 40}{RESET}\n")

while True:

    response = client.chat.completions.create(
        model="deepseek-flash", messages=messages, tools=tools
    )

    message = response.choices[0].message

    messages.append(message)

    if message.tool_calls:

        for tool_call in message.tool_calls:

            print(tool_call.function.name)

            try:
                args = json.loads(tool_call.function.arguments)

                result = functions[tool_call.function.name](**args)

            except Exception as e:

                result = f"Error: {type(e).__name__}: {e}"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    else:

        print(message.content)

        iterations += 1

        if iterations == 4:
        
                break

        BOLD_CYAN = "\033[1;96m"
        RESET = "\033[0m"

        print(f"\n{BOLD_CYAN}{'=' * 40}")
        print(f"  ITERATION {iterations}")
        print(f"{'=' * 40}{RESET}\n")

        messages.append({"role": "user", "content": f"iteration: {iterations}"})
        
        

    