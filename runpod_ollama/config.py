from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


def get_env_or_throw(env_name: str, default_value: str = None) -> str:
    env_value = os.getenv(env_name)
    if not env_value:
        if default_value is not None:
            return default_value
        raise Exception(f"Environment variable {env_name} not set")
    return env_value


@dataclass
class ENVIRONMENT:
    RUNPOD_API_TOKEN = get_env_or_throw("RUNPOD_API_TOKEN", default_value="test_mode_token")
    HF_TOKEN = get_env_or_throw("HF_TOKEN", default_value=None)
    # OPEN_AI_API_KEY = get_env_or_throw("OPEN_AI_API_KEY")
