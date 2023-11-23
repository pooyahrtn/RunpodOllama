import time
from typing import Any, Dict, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.chat_models.base import BaseChatModel
from langchain.schema import ChatResult, ChatGeneration
from langchain.schema.messages import BaseMessage
import requests
from langchain.schema.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)


class RunpodRepository:
    def __init__(self, api_key: str, pod_id: str):
        self.api_key = api_key
        self.pod_id = pod_id
        self.active_request_id: Optional[str] = None

    def generate(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = self._request_headers()
        default_stop = ["<|im_start|>", "<|im_end|>"]
        input = {
            "method_name": "generate",
            "input": {
                "prompt": prompt,
                "options": {"stop": (stop or []) + default_stop},
            },
        }

        # TODO: Handle network errors
        out = requests.post(
            f"{self._request_base_url()}/run",
            headers=headers,
            json={"input": input},
        ).json()

        self.active_request_id = out["id"]

        while out["status"] != "COMPLETED":
            out = requests.get(
                f"{self._request_base_url()}/status/{self.active_request_id}",
                headers=headers,
            ).json()
            time.sleep(1)

        return out["output"]["response"]

    def cancel_requests(self):
        if not self.active_request_id:
            return
        headers = self._request_headers()

        return requests.post(
            f"{self._request_base_url()}/cancel/{self.active_request_id}",
            headers=headers,
        )

    def _request_base_url(self) -> str:
        return f"https://api.runpod.ai/v2/{self.pod_id}"

    def _request_headers(self) -> Mapping[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.api_key,
        }


class RunpodServerlessLLM(LLM):
    pod_id: str
    api_key: str

    @property
    def _llm_type(self) -> str:
        return "runpod-serverless"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        response = self._runpod_repository.generate(prompt, stop=stop)
        return response

    @property
    def _runpod_repository(self) -> RunpodRepository:
        return RunpodRepository(api_key=self.api_key, pod_id=self.pod_id)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"pod_id": self._runpod_repository.pod_id}


class ChatRunpodServerless(BaseChatModel):
    pod_id: str
    api_key: str

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: List[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompts = list(map(self._convert_one_message_to_text, messages))

        result = self._llm.generate(
            prompts=prompts,
            stop=stop,
        ).generations[
            0
        ][0]

        chat_generation = ChatGeneration(
            message=AIMessage(content=result.text),
            generation_info=result.generation_info,
        )
        return ChatResult(generations=[chat_generation])

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "runpod-serverless-chat"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {"pod_id": self.pod_id}

    @property
    def _llm(self) -> LLM:
        return RunpodServerlessLLM(pod_id=self.pod_id, api_key=self.api_key)

    def _convert_one_message_to_text(self, message: BaseMessage) -> str:
        if isinstance(message, ChatMessage):
            message_text = f"\n\n{message.role.capitalize()}: {message.content}"
        elif isinstance(message, HumanMessage):
            message_text = f"[INST] {message.content} [/INST]"
        elif isinstance(message, AIMessage):
            message_text = f"{message.content}"
        elif isinstance(message, SystemMessage):
            message_text = f"<<SYS>> {message.content} <</SYS>>"
        else:
            raise ValueError(f"Got unknown type {message}")
        return message_text
