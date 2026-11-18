import os
from dotenv import load_dotenv

load_dotenv()

PROVIDERS = {

    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "model": "deepseek-flash",
    },

    "anthropic": {
    "base_url": "https://api.anthropic.com/v1/",
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "model": "claude-haiku-5-5",
     },

    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama", 
        "model": "qwen3-4b",
    },
}
