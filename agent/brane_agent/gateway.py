"""BRANE gateway client — the ONLY way this agent reaches a language model.

There is deliberately no OpenAI client in this code base and no fallback path:
any error, timeout, missing configuration or block decision raises and the
pipeline sends nothing (R10, fail-closed).

ASSUMPTION (unverified): BRANE exposes an OpenAI-compatible
`POST {BRANE_API_URL}/v1/chat/completions` endpoint authenticated with
`Authorization: Bearer {BRANE_API_KEY}`. Replace `_build_request` /
`_parse_response` once the real BRANE API docs are available. Nothing else
in the agent needs to change.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class GatewayUnavailable(Exception):
    """BRANE could not be reached or returned an error -> nothing is sent."""


class GatewayBlocked(Exception):
    """BRANE inspected the request and refused it."""


class BraneGateway:
    def __init__(self, url: str | None = None, api_key: str | None = None,
                 model: str | None = None, timeout: float = 20.0):
        self.url = (url if url is not None else os.environ.get("BRANE_API_URL", "")).rstrip("/")
        self.api_key = api_key if api_key is not None else os.environ.get("BRANE_API_KEY", "")
        self.model = model or os.environ.get("BRANE_MODEL", "gpt-4o-mini")
        self.timeout = timeout

    def _build_request(self, messages: list[dict]) -> urllib.request.Request:
        body = json.dumps({"model": self.model, "messages": messages, "temperature": 0}).encode()
        return urllib.request.Request(
            f"{self.url}/v1/chat/completions",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
        )

    @staticmethod
    def _parse_response(raw: bytes) -> str:
        data = json.loads(raw)
        if data.get("blocked") or data.get("decision") == "block":
            raise GatewayBlocked(data.get("reason", "blocked by BRANE policy"))
        return data["choices"][0]["message"]["content"]

    def complete(self, messages: list[dict]) -> str:
        if not self.url or not self.url.startswith(("http://", "https://")):
            raise GatewayUnavailable("BRANE_API_URL not configured")
        try:
            with urllib.request.urlopen(self._build_request(messages), timeout=self.timeout) as r:
                return self._parse_response(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 451):
                raise GatewayBlocked(f"BRANE refused request (HTTP {e.code})") from e
            raise GatewayUnavailable(f"BRANE error HTTP {e.code}") from e
        except GatewayBlocked:
            raise
        except Exception as e:  # network error, timeout, bad JSON... -> fail closed
            raise GatewayUnavailable(f"{type(e).__name__}: {e}") from e
