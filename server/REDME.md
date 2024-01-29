# Server

This folder is running on the server.
The Dockerfile starts the Ollama server, then executes the `runpod_wrapper`.
`runpod_wrapper` forwards the requests to the Ollama server.
