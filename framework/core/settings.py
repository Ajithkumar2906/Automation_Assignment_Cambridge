"""Centralized runtime settings for the automation framework."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable configuration loaded from environment variables."""

    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com/")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    remote: bool = os.getenv("REMOTE", "false").lower() == "true"
    selenium_grid_url: str = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444/wd/hub")
    implicit_wait: int = int(os.getenv("IMPLICIT_WAIT", "2"))
    explicit_wait: int = int(os.getenv("EXPLICIT_WAIT", "15"))
    window_width: int = int(os.getenv("WINDOW_WIDTH", "1920"))
    window_height: int = int(os.getenv("WINDOW_HEIGHT", "1080"))
    action_delay_seconds: float = float(os.getenv("ACTION_DELAY_SECONDS", "0.35"))
    step_delay_seconds: float = float(os.getenv("STEP_DELAY_SECONDS", "0.8"))


settings = Settings()
