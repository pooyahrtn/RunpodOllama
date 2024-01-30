"""Example of using litellm to run a pod on a local server.

1. Run poetry install --all-extras
2. Run the local-proxy with

```
$ runpod-ollama start-proxy
```
"""

import litellm

response = litellm.completion(
    "ollama/mixtral",
    messages=[
        {"content": "why the sky is blue?"},
    ],
    base_url="http://127.0.0.1:5001/mpsuuw648lsi2z",
    stream=False,
)

print(response.choices[0].message["content"])  # type: ignore
