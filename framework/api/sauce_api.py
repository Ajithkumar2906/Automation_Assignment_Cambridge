"""Lightweight API/HTTP checks to complement UI coverage."""

from __future__ import annotations

from urllib.parse import urljoin

import requests

from framework.core.settings import settings


class ApiClientError(RuntimeError):
    """Raised when API request/response handling fails."""


class SauceApiClient:
    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.base_url = settings.api_base_url.rstrip("/") + "/"

    def _build_url(self, endpoint: str) -> str:
        return urljoin(self.base_url, endpoint.lstrip("/"))

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        url = self._build_url(endpoint)
        try:
            return self.session.get(url, params=params, timeout=self.timeout)
        except requests.RequestException as exc:
            raise ApiClientError(f"API GET failed for {url}: {exc}") from exc

    def get_json(self, endpoint: str, params: dict | None = None) -> tuple[int, dict | list]:
        response = self.get(endpoint, params=params)
        try:
            return response.status_code, response.json()
        except ValueError as exc:
            text = (response.text or "")[:250]
            raise ApiClientError(
                f"Expected JSON from {response.url} but got non-JSON response. "
                f"status={response.status_code} body_prefix={text!r}"
            ) from exc

    def get_login_page_status(self) -> int:
        response = requests.get(settings.base_url, timeout=self.timeout)
        return response.status_code

    def get_login_page_text(self) -> str:
        response = requests.get(settings.base_url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def get_inventory(self, sort_value: str) -> tuple[int, dict | list]:
        return self.get_json(settings.api_inventory_endpoint, params={"sort": sort_value})

    def get_cart(self) -> tuple[int, dict | list]:
        return self.get_json(settings.api_cart_endpoint)

    def get_latest_order(self) -> tuple[int, dict | list]:
        return self.get_json(settings.api_latest_order_endpoint)
