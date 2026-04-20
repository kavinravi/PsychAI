#!/usr/bin/env python
"""
Quick smoke test that the configured PsychAI endpoint/model returns a reply.

Reads the same secrets the Streamlit app does, so if this works the app will
work too.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "website"))

# Stub minimal Streamlit shim so utils.model_inference can import.
import types

st_shim = types.ModuleType("streamlit")


def _cache_resource(*a, **kw):
    if a and callable(a[0]):
        return a[0]
    def deco(f):
        return f
    return deco


st_shim.cache_resource = _cache_resource


class _Secrets(dict):
    def get(self, k, default=None):
        return super().get(k, default)


def _load_secrets() -> _Secrets:
    p = Path(__file__).resolve().parent.parent / "website" / ".streamlit" / "secrets.toml"
    if not p.exists():
        return _Secrets()
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore
    with p.open("rb") as f:
        return _Secrets(tomllib.load(f))


st_shim.secrets = _load_secrets()
sys.modules["streamlit"] = st_shim

from utils.model_inference import generate_reply  # noqa: E402

prompt = "I've been feeling really anxious about school lately. Any advice?"
print(f"USER: {prompt}\n")
print("PSYCHAI:", generate_reply(prompt, []))
