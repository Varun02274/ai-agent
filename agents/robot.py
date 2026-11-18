import os
import io
import json
import time
from contextlib import redirect_stdout
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from tools import tools, functions

load_dotenv()
console = Console()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = (Path(__file__).parent.parent/"prompts" / "system.md").read_text(encoding="utf-8")

# ---------- moods ----------

MOODS = {
    "idle":     ("◉ ◉", "───", "cyan"),
    "thinking": ("◔ ◔", "···", "yellow"),
    "happy":    ("^ ^", "◡◡◡", "green"),
    "excited":  ("★ ★", "◠◠◠", "bright_magenta"),
    "curious":  ("◉ ◎", " o ", "blue"),
    "sad":      ("╥ ╥", "╭─╮", "bright_blue"),
    "angry":    ("▼ ▼", "═══", "red"),
    "sleepy":   ("- -", "───", "grey62"),
}
SELECTABLE = [m for m in MOODS if m != "thinking"]

MOOD_TOOL = {
    "type": "function",
    "function": {
        "name": "set_mood",
        "description": "Set the mood shown on your robot face in the terminal. "
                       "You can change moods at any point during the conversation.",
        "parameters": {
            "type": "object",
            "properties": {"mood": {"type": "string", "enum": SELECTABLE}},
            "required": ["mood"],
        },
    },
}

# ---------- display ----------

MAX_BUBBLE_ITEMS = 12


class Display:
    def __init__(self):
        self.mood = "idle"
        self.busy = False
        self.iteration = 1
        self.bubble = []

    def say(self, renderable):
        self.bubble.append(renderable)
        self.bubble = self.bubble[-MAX_BUBBLE_ITEMS:]

    def robot(self, mood):
        eyes, mouth, color = MOODS[mood]
        dim = f"dim {color}"
        bold = f"bold {color}"
        screen = "on grey11"

        # antenna bulb blinks while thinking
        blink = mood == "thinking" and int(time.time() * 2) % 2
        bulb = "○" if blink else "●"

        t = Text(no_wrap=True)

        def line(*parts):
            for text, style in parts:
                t.append(text, style=style)
            t.append("\n")

        pad = " " * 9
        line(("        ", ""), (bulb, bold))
        line(("        ", ""), ("│", dim))
        line(("  ╭─────┴─────╮", color))
        line(("  │ ", color), (pad, screen), (" │", color))
        line(("▐█", dim), ("│ ", color), (f"   {eyes}   ", f"{bold} {screen}"), (" │", color), ("█▌", dim))
        line(("  │ ", color), (f"   {mouth}   ", f"{bold} {screen}"), (" │", color))
        line(("  ╰─────┬─────╯", color))
        line(("        ", ""), ("║", dim))
        line(("   ╭─────┴───╮", color))
        line(("   │ ", color), ("▪", bold), (" ", ""), ("▪", dim), (" ", ""), ("▪", bold), ("   │", color))
        line(("   ╰─────────╯", color))
        line(("   ▄▄▄     ▄▄▄", dim))
        t.rstrip()

        return Panel(t, border_style=color, subtitle=mood, expand=False, padding=(0, 1))

    def __rich__(self):
        mood = self.mood
        color = MOODS[mood][2]

        items = list(self.bubble)
        if self.busy:
            items.append(Text("thinking" + "." * (int(time.time() * 3) % 4), style="italic yellow"))
        if not items:
            items.append(Text("..."))

        bubble = Panel(
            Group(*items),
            title=f"iteration {self.iteration}",
            title_align="left",
            border_style=color,
            box=box.ROUNDED,
            padding=(0, 1),
        )

        grid = Table.grid(padding=(0, 0))
        grid.add_column()
        grid.add_column(vertical="middle")
        grid.add_column(ratio=1)
        grid.add_row(self.robot(mood), Text("◀", style=color), bubble)
        return grid


ui = Display()


def set_mood(mood: str):
    if mood not in SELECTABLE:
        return f"Unknown mood. Choose from: {', '.join(SELECTABLE)}"
    ui.mood = mood
    return f"mood set to {mood}"


all_tools = tools + [MOOD_TOOL]
all_functions = {**functions, "set_mood": set_mood}

# ---------- agent loop ----------

iterations = 1
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"iteration: {iterations}"},
]

with Live(ui, console=console, refresh_per_second=12,
          vertical_overflow="visible", redirect_stdout=False):
    while True:
        ui.busy = True
        response = client.chat.completions.create(
            model="deepseek-chat", messages=messages, tools=all_tools
        )
        ui.busy = False

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                buf = io.StringIO()
                try:
                    args = json.loads(tool_call.function.arguments)
                    if name != "set_mood":
                        ui.say(Text(f"→ {name}({', '.join(f'{k}={v!r}' for k, v in args.items())})", style="dim"))
                    with redirect_stdout(buf):          # capture print() calls inside tools
                        result = all_functions[name](**args)
                except Exception as e:
                    result = f"Error: {type(e).__name__}: {e}"
                    ui.say(Text(result, style="red"))

                printed = buf.getvalue().strip()
                if printed:
                    ui.say(Text(printed))

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )
        else:
            ui.say(Markdown(message.content or ""))

            iterations += 1
            if iterations > 5:
                break

            ui.iteration = iterations
            ui.say(Text(f"── iteration {iterations} ──", style="dim"))
            messages.append({"role": "user", "content": f"iteration: {iterations}"})