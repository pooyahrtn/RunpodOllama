# https://api.runpod.ai/v2/{self.pod_id}
from runpod_ollama.config import ENVIRONMENT
from runpod_ollama.runpod_repository import RunpodRepository

runpod_repository = RunpodRepository(
    api_key=ENVIRONMENT.RUNPOD_API_TOKEN,
    pod_id="nla971fm35t2ck",
)

# Later we can modify the Docker to pull the model later.
# Right now, the server overrides the model with the one included in the command.
runpod_repository.pull_model("phi")
