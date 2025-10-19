from __future__ import annotations

import os
import subprocess
import sys

import pytest


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="requires OPENAI_API_KEY")
def test_cli_ask_runs():
    env = os.environ.copy()
    # Prefer dummy model env to minimize cost if possible
    env.setdefault("OPENAI_MODEL", "gpt-4o-mini")

    result = subprocess.run(
        [sys.executable, "-m", "ai_bots.cli", "ask", "What is the return window?"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() != ""
