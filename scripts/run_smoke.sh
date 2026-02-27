#!/usr/bin/env bash
set -euo pipefail

pytest -m smoke --alluredir=reports/allure-results
