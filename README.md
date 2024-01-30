# Running Ollama with Runpod Serverless

## How it works

```mermaid
sequenceDiagram
    box Client
    participant Client (e.g. litellm)
    participant Local Proxy
    end
    box Server
    participant Runpod
    participant Ollama
    end
    Client (e.g. litellm)->>Local Proxy: Call Ollama API
    Local Proxy->>Runpod: Forwards Ollama API call
    Runpod->>Ollama: Forwards Ollama API call
    loop Check every second
        Local Proxy --> Runpod: Check request status
    end
    Ollama-->>Runpod: Ollama responds
    Runpod-->>Local Proxy: Forwards Ollama response
    Local Proxy-->>Client (e.g. litellm): Receives Ollama response
```

### Ollama

## Blog

Check the blog [here](https://medium.com/@pooya.haratian/running-ollama-with-runpod-serverless-and-langchain-6657763f400d)

# Setup

1. Create a serverless endpoint (check blog)
   1. Create a template with `pooyaharatian/runpod-ollama:0.0.4` image
   2. In the Docker command, put the model name. E.g. `codellama:7b-instruct-q5_K_M`
2. Make sure you have poetry installed

# Examples

To run the examples, first install the examples dependencies:

```
$ poetry install --all-extras
```
