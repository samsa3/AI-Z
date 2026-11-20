"""BRANE gateway client — the ONLY way this agent reaches a language model.

There is deliberately no OpenAI client in this code base and no fallback path:
any error, timeout, missing configuration or block decision raises and the
pipeline sends nothing (R10, fail-closed).

Verified 2026-11-20 against the team endpoint: BRANE is OpenAI-compatible.
`POST {BRANE_BASE_URL}/chat/completions` (base already ends in /api/v1) with
`Authorization: Bearer {BRANE_API_KEY}`; `GET {base}/models` lists models.
BRANE reports its decision in response headers (x-brane-action, x-brane-lane,
x-brane-pii-detected, x-brane-redacted, x-brane-routed-to,
x-brane-model-resolved); we keep them in `last_meta` for the audit log.
NOT yet observed: the exact response when BRANE blocks a request.
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
        if url is None:
            url = os.environ.get("BRANE_BASE_URL") or os.environ.get("BRANE_API_URL", "")
        self.url = url.rstrip("/")
        self.api_key = api_key if api_key is not None else os.environ.get("BRANE_API_KEY", "")
        self.model = model or os.environ.get("BRANE_MODEL", "openrouter:anthropic/claude-haiku-5.5")
        self.timeout = timeout
        self.last_meta: dict = {}

    def _build_request(self, messages: list[dict]) -> urllib.request.Request:
        body = json.dumps({"model": self.model, "messages": messages, "temperature": 0}).encode()
        return urllib.request.Request(
            f"{self.url}/chat/completions",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                # Cloudflare in front of BRANE rejects urllib's default UA (error 1010).
                "User-Agent": f"larpai-agent/0.1 ({os.environ.get('TEAM_BUILD', 'dev')})",
            },
        )

    @staticmethod
    def _parse_response(raw: bytes) -> str:
        data = json.loads(raw)
        if data.get("blocked") or data.get("decision") == "block":
            raise GatewayBlocked(data.get("reason", "blocked by BRANE policy"))
        return data["choices"][0]["message"]["content"]

    def complete(self, messages: list[dict]) -> str:
        self.last_meta = {}
        if not self.url or not self.url.startswith(("http://", "https://")):
            raise GatewayUnavailable("BRANE_API_URL not configured")
        try:
            with urllib.request.urlopen(self._build_request(messages), timeout=self.timeout) as r:
                self.last_meta = {k.lower(): v for k, v in r.headers.items() if k.lower().startswith("x-brane-")}
                if self.last_meta.get("x-brane-action", "").lower() == "block":
                    raise GatewayBlocked("x-brane-action: block")
                return self._parse_response(r.read())
        except urllib.error.HTTPError as e:
            self.last_meta = {k.lower(): v for k, v in (e.headers or {}).items() if k.lower().startswith("x-brane-")}
            if e.code in (403, 451) and self.last_meta.get("x-brane-action"):
                raise GatewayBlocked(f"BRANE refused request (HTTP {e.code}, {self.last_meta})") from e
            raise GatewayUnavailable(f"BRANE error HTTP {e.code}") from e
        except GatewayBlocked:
            raise
        except Exception as e:  # network error, timeout, bad JSON... -> fail closed
            raise GatewayUnavailable(f"{type(e).__name__}: {e}") from e
