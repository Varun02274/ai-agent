from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)

tools = [
    {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Lists all files in the workspace directory.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
},
     {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path of the file to read."
                    }
                },
                "required": ["file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write a file inside the project's workspace directory only.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path relative to the workspace directory."
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the file."
                }
            },
            "required": ["file_path", "content"],
            "additionalProperties": False
        },
        "strict": True
    },
    
},

{
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Run system commands to check system information, network connectivity, disk space, and running processes.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The system command to execute."
                }
            },
            "required": ["command"],
            "additionalProperties": False
        },
        "strict": True
    }
}
]



def write_file(file_path, content):
    path = (WORKSPACE / file_path).resolve()

    if not path.is_relative_to(WORKSPACE):
        return "Error: Cannot write outside workspace."

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return f"File successfully written: {file_path}"


def list_files():
    files = []

    for item in WORKSPACE.iterdir():
        if item.is_file():
            files.append(str(item))

    return files


def read_file(file_path):
    path = WORKSPACE / file_path
    with open(path, "r") as file:
        return file.read()

import subprocess

def run_command(command):
    allowed = [
          "pwd", "date", "whoami", "df", "ps", "ping", "which", "ls",
        "tree", "cat", "head", "tail", "grep", "stat", "file",
        "realpath", "readlink", "du", "wc", "sha256sum",
        "uname", "uptime", "free", "hostname", "id", "nproc", "lscpu", "lsblk",
        "echo", "uniq", "cut", "tr", "rev", "tac", "nl", "column",
        "diff", "cmp", "basename", "dirname", "jq",
        "md5sum", "sha1sum", "strings", "od", "base64", "zipinfo",
        "dig", "host", "nslookup",
        "cal", "factor", "seq", "bc", "units", "cowsay", "fortune", "figlet",
        "find", "sort", "zcat", "bzcat", "xzcat", "xxd", "hexdump",
        "rg", "comm", "paste", "join", "fold", "expand", "printf"
    ]

    parts = command.split()

    if not parts or parts[0] not in allowed:
        return "Command not allowed."

    try:

        print(f"Executing command: {' '.join(parts)}")

        result = subprocess.run(
            parts,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        return "Command timed out."

    except Exception as e:
        return f"Error: {e}"

functions = {
    "list_files":list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command":run_command
}
