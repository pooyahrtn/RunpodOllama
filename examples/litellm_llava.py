"""Example of using litellm to run a pod on a local server.

1. Run poetry install --all-extras
2. Run the local server to forward requests to runpod:
```
$ poetry run local_proxy
```
"""

import litellm

response = litellm.completion(
    "ollama/runpod",
    messages=[
        {"content": "why the sky is blue?"},
    ],
    base_url="http://127.0.0.1:5000/nla971fm35t2ck",
    stream=False,
)

print(response.choices[0].message["content"])  # type: ignore
