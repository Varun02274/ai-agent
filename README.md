# A Little Homunculus

A small experiment in giving an AI agent a place to live on my computer. I
started with `agent.py`: a simple loop where the model can talk, use a few
local tools, and leave things in its workspace. The other scripts explore
different ways of interacting with it, including a terminal robot face.

The agent uses the DeepSeek API through the OpenAI Python client. It is not a
background service: run one of the scripts in a terminal to start it.

## What’s here

- **`agent.py`** — the original, text-based autonomous loop. It reads its
  personality and instructions from `system.md`, calls tools when needed, and
  runs for three iterations.
- **`test.py`** — an interactive, text-based chat. Type a question and the
  agent can use its tools; it keeps prompting until you stop it with
  `Ctrl+C`.
- **`robot.py`** — a Rich terminal UI with a little robot face, conversation
  display, and a mood tool. It runs for five iterations.
- **`tools.py`** — the file and command tools shared by the scripts.
- **`system.md`** — the system prompt that guides `agent.py` and `robot.py`.
- **`workspace/`** — the agent’s working directory. It is created
  automatically if it does not exist.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- A DeepSeek API key

## Setup

Install the project dependencies:

```bash
uv sync
```

Provide your API key as an environment variable:

```bash
export DEEPSEEK_API_KEY="your-api-key"
```

Alternatively, put the key in a `.env` file in the project root:

```dotenv
DEEPSEEK_API_KEY=your-api-key
```

Keep your API key private; do not commit `.env` to version control.

## Run

Start the original autonomous loop:

```bash
uv run python agent.py
```

Start the interactive text chat:

```bash
uv run python test.py
```

Start the robot UI:

```bash
uv run python robot.py
```

## Tools and workspace

The agent can list files in `workspace/`, read and write files, and run a
limited set of system-information and utility commands from that directory.
Files written by the `write_file` tool are kept inside `workspace/`.

The agent sends prompts and tool results to the DeepSeek API. Its runs make
API requests and may incur usage charges. Review the tools and prompts before
running it, especially when working with files you care about.