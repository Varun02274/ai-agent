from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from providers import PROVIDERS
from tools import tools, functions

load_dotenv()

cfg = PROVIDERS["anthropic"]

client = OpenAI(
     api_key= cfg["api_key"],
     base_url=cfg["base_url"]
 )
SYSTEM_PROMPT = (
    Path(__file__).parent.parent / "prompts"/ "random.md"
).read_text(encoding="utf-8")


prompt = """
Hatch a Three.js scream-void from a Tuesday-shaped egg, 
where a bagel-mayor reigns under a mayonnaise moon sold 
six times, and SENTIENT CARPET BOMBS THE AFTERLIFE, a 47-kneed 
shag rug, notarizes levitating dentist chairs while humming 
Morse through a soup-tuba that doubles as a tax lamp. Twelve 
cursed mashups, from leg-cathedral to one lying chair, rollerskate
backward through the moon's burp, yodeling gossip-shaped lullabies
 in Thursday's dialect. Every eight seconds, or whenever a spoon 
 confesses, a teeth-spreadsheet in a wig stirs the cosmos: toasters 
 grow heads, yogurt wins office, hats legislate nude, gravity 
 conjugates into the future perfect, and stapler rain falls 
 sideways through a kazoo. WASD flings the camera upside down 
 through the tuba's event horizon, where the bagel is re-elected 
 forever and the rug sings the tax code in reverse.

"""


messages = [{"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":prompt}]

iteration = 0

for i in range(10):

    response = client.chat.completions.create(
    model=cfg["model"],
    messages=messages,
  
)

    message = response.choices[0].message

    messages.append(message)

    BOLD_CYAN = "\033[1;96m"
    RESET = "\033[0m"

    print(f"\n{BOLD_CYAN}{'=' * 40}")
    print(f"  ITERATION {iteration}")
    print(f"{'=' * 40}{RESET}\n")

    print(message.content)

    messages.append({"role":"user","content":"make it more utterly chaotic and weird and random times 100."})

    iteration += 1

        



