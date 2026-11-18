# AI Agent Playground

A collection of experimental Python agents that use OpenAI-compatible chat APIs to demonstrate tool calling, autonomous iteration, prompt-driven workflows, and terminal UI rendering.

The project includes a general-purpose agent, a file-finding puzzle agent, a prompt-chaos generator, and an interactive Rich terminal robot.

## Features

- **Tool calling:** Agents can list files, read files, write files, and run a restricted set of system commands.
- **Multiple model providers:** Configuration for DeepSeek, Anthropic, and a local Ollama server.
- **Workspace sandbox:** File operations are scoped to `agents/workspace`.
- **Command allowlist:** Shell commands are restricted by an explicit allowlist.
- **Rich terminal UI:** `robot.py` renders iterations and tool activity in a live robot interface.
- **Prompt experiments:** Separate system prompts support autonomous tasks and random prompt generation.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/) for environment and dependency management
- API credentials for the provider you use
- Ollama for the local-provider configuration

The project dependencies are defined in `pyproject.toml`:

- `openai`
- `python-dotenv`
- `rich`

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Varun02274/ai-agent.git
cd ai-agent
uv sync
```

`uv sync` creates or updates the local `.venv` environment and installs the locked dependencies.

## Configuration

Create a `.env` file in the repository root:

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

The provider settings are defined in `agents/providers.py`:

| Provider | Base URL | Default model |
|---|---|---|
| DeepSeek | `https://api.deepseek.com` | `deepseek-flash` or `deepseek-chat` |
| Anthropic | `https://api.anthropic.com/v1/` | `claude-haiku-5-5` |
| Ollama | `http://localhost:11434/v1` | `qwen3-4b` |

Only providers selected by each script are used by default. Keep API keys in `.env`; the file is excluded by `.gitignore`.

## Running the Agents

Run scripts from the repository root:

### General autonomous agent

```bash
uv run python agents/agent.py
```

This loads `prompts/system.md`, uses the DeepSeek provider configuration, and runs for five user-controlled iterations.

### Puzzle agent

```bash
uv run python agents/puzzle.py
```

This loads `prompts/puzzle.md` and instructs the model to search for a hidden key in the local environment and write it to `agents/workspace/key.md`.

### Rich terminal robot

```bash
uv run python agents/robot.py
```

This runs a five-iteration interactive display with:

- Markdown-formatted model responses
- Tool-call and command output
- A live mood indicator
- The `set_mood` function

### Prompt chaos generator

```bash
uv run python agents/random_agent.py
```

This uses Anthropic configuration and sends ten increasingly chaotic rewrite requests based on `prompts/random.md`.

## Available Tools

Tools are declared and implemented in `agents/tools.py`.

| Tool | Description |
|---|---|
| `list_files` | Lists files directly inside `agents/workspace` |
| `read_file` | Reads a file relative to `agents/workspace` |
| `write_file` | Writes a file inside `agents/workspace` |
| `run_command` | Runs an allowlisted command with a 30-second timeout |

`write_file` resolves paths and prevents writes outside the workspace. `read_file` accepts a workspace-relative path. `run_command` supports safe inspection and text-processing commands such as `ls`, `find`, `cat`, `grep`, `stat`, `ps`, `df`, and `ping`.

Commands are executed in `agents/workspace`, and commands not in the allowlist are rejected.

## Project Structure

```text
.
├── agents/
│   ├── agent.py          # Five-iteration general agent loop
│   ├── providers.py      # Provider API configuration
│   ├── puzzle.py         # Hidden-key puzzle workflow
│   ├── random_agent.py   # Chaotic prompt generator
│   ├── robot.py          # Rich terminal robot UI
│   ├── tools.py          # Tool schemas and implementations
│   └── workspace/        # Sandboxed file and command directory
├── prompts/
│   ├── puzzle.md         # Puzzle-agent instructions
│   ├── random.md         # Prompt randomization instructions
│   └── system.md         # General-agent instructions
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # Reproducible dependency lockfile
└── .python-version       # Python 3.14
```

## Development Notes

- Provider configuration uses `python-dotenv`, so environment variables can be loaded from `.env`.
- Scripts using `tool_calls` return tool results as JSON to the model conversation.
- The agent loops stop after a fixed number of iterations or when the model sends no tool call.
- Tool exceptions are converted into errors and sent back to the model.
- The workspace directory is created automatically when `agents/tools.py` is imported.

## Security

Do not commit `.env`, API keys, or files containing sensitive workspace results. Although file writes and command execution are restricted in this project, generated agents can still interact with local state through allowed tools. Review provider usage and prompts before running them.
