# Running Ollama with Runpod Serverless and LangChain

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
