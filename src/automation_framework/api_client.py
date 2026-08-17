"""Dependency-light JSON client for service-level test assertions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class ApiResponse:
    status_code: int
    body: Any
    headers: dict[str, str]


class ApiClient:
    """Make JSON GET requests against the system under test."""

    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

    def get(self, path: str) -> ApiResponse:
        url = urljoin(self.base_url, path.lstrip("/"))
        request = Request(url, headers={"Accept": "application/json"})
        with urlopen(request, timeout=self.timeout) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
            return ApiResponse(
                status_code=response.status,
                body=payload,
                headers=dict(response.headers.items()),
            )
