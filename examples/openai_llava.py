"""Example of using the OpenAI client with the Llava model.

1. Make sure you started the local proxies (run /scripts/start-proxy.sh)
2. The initial request might take longer or fail as the server is fetching the model
3. Make sure you've updated the config
"""

import openai

client = openai.OpenAI(
    api_key="sk-j6",  # Some dummy value to
    base_url="http://0.0.0.0:8000",
)

response = client.completions.create(
    # The model name should ALWAYS be "ollama/mistral".
    # This is misleading, but it's needed to trick LiteLLM into using
    # the Ollama model.
    # At the end, the model that's defined in the Runpod is used.
    model="ollama/mistral",
    prompt="why the sky is blue?",
)

print(response.choices[0].message["content"])
