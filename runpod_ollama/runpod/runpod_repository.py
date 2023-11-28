import time
from typing import Mapping, Optional, Any
import requests


class RunpodRepository:
    def __init__(self, api_key: str, pod_id: str):
        self.api_key = api_key
        self.pod_id = pod_id
        self.active_request_id: Optional[str] = None

    def generate(self, input: Any) -> Mapping[str, Any]:
        headers = self._request_headers()
        input = {
            "method_name": "generate",
            "input": input,
        }

        # TODO: Handle network errors
        response = requests.post(
            f"{self._request_base_url()}/run",
            headers=headers,
            json={"input": input},
        )
        response.raise_for_status()
        out = response.json()
        self.active_request_id = out["id"]

        while out["status"] != "COMPLETED":
            out = requests.get(
                f"{self._request_base_url()}/status/{self.active_request_id}",
                headers=headers,
            ).json()
            time.sleep(1)

        return out["output"]

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
