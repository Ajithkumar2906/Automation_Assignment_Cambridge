"""Lightweight API/HTTP checks to complement UI coverage."""

from __future__ import annotations

import requests

from framework.core.settings import settings


class SauceApiClient:
    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

    def get_login_page_status(self) -> int:
        response = requests.get(settings.base_url, timeout=self.timeout)
        return response.status_code

    def get_login_page_text(self) -> str:
        response = requests.get(settings.base_url, timeout=self.timeout)
        response.raise_for_status()
        return response.text
