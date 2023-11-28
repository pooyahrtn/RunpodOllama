from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


def get_env_or_throw(env_name: str) -> str:
    env_value = os.getenv(env_name)
    if not env_value:
        raise Exception(f"Environment variable {env_name} not set")
    return env_value


@dataclass
class ENVIRONMENT:
    RUNPOD_API_TOKEN = get_env_or_throw("RUNPOD_API_TOKEN")
    # OPEN_AI_API_KEY = get_env_or_throw("OPEN_AI_API_KEY")
