import json
from openai import OpenAI
 
client = OpenAI()  # reads OPENAI_API_KEY from your environment
MODEL = "gpt-4o-mini"
 
 
# ---------- 1. The tools (plain Python functions) ----------
 
def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"
 
 
def write_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error: {e}"
 
 
# Map tool names to the functions above
TOOL_FUNCTIONS = {
    "read_file": read_file,
    "write_file": write_file,
}
 
 
# ---------- 2. Tool descriptions (what the model sees) ----------
 
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path of the file to read"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file (overwrites it if it exists).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path of the file to write"},
                    "content": {"type": "string", "description": "Text to write into the file"},
                },
                "required": ["path", "content"],
            },
        },
    },
]
 
 
# ---------- 3. The agent loop ----------
 
def run_agent(messages):
    """Keep calling the model until it stops asking for tools."""
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message)  # save the model's reply in the history
 
        # No tool calls means the model is done and gave a final answer
        if not message.tool_calls:
            return message.content
 
        # Otherwise, run each tool the model asked for
        for call in message.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"  [tool] {name}({args})")
 
            result = TOOL_FUNCTIONS[name](**args)
  
            # Send the result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })
        # Loop again so the model can see the tool results
 
 
# ---------- 4. Chat with the agent ----------
 
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can read and write files."}
    ]
 
    print("Agent ready. Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ("quit", "exit"):
            break
 
        messages.append({"role": "user", "content": user_input})
        answer = run_agent(messages)
        print(f"\nAgent: {answer}")