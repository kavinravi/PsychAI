"""
Model inference for PsychAI

Calls the fine-tuned Qwen3-8B + PsychAI LoRA via the Hugging Face
``InferenceClient`` over HTTP. Three deployment modes are supported, in order
of preference:

1. **Dedicated Inference Endpoint** — set ``[huggingface] endpoint_url`` to the
   ``*.endpoints.huggingface.cloud`` URL you get after deploying the model on
   https://ui.endpoints.huggingface.co/. Recommended for custom LoRAs.
2. **Inference Providers (serverless)** — set ``[huggingface] provider`` to
   ``"auto"`` (or a specific provider like ``"hf-inference"`` /
   ``"together"``) and HF will route the request to whichever provider hosts
   the model.
3. **Plain serverless Inference API** — fallback when neither of the above is
   set; only works if the model is "warm" on the free Inference API.

No local GPU, ``torch``, ``peft``, or ``bitsandbytes`` is needed at runtime.
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional

import streamlit as st
from huggingface_hub import InferenceClient


SYSTEM_PROMPT = (
    'You are "PsychAI," a compassionate coach who supports teens dealing with '
    "anxiety, mood dips, and everyday stresses. "
    "Always validate the user\u2019s feelings and invite self-reflection before offering guidance. "
    "Share coping ideas, grounding techniques, or resources, "
    "but never diagnose, prescribe medication, or promise confidentiality. "
    "When you suspect safety risks or crises, encourage the teen to reach out to a trusted adult "
    "or emergency professional immediately. "
    "Keep replies in one or two conversational paragraphs "
    "(no bullet lists unless the user explicitly asks), avoid clinical jargon, "
    "and sound warm, hopeful, and practical. "
    "End by inviting the user to share how the suggestion felt or ask a follow-up question."
)

DEFAULT_MODEL_ID = "kavin-ravi/qwen3-8b-psychai-merged"


def _hf_setting(key: str, default=None):
    """Read a key from the [huggingface] secrets table, falling back to env."""
    try:
        section = st.secrets.get("huggingface", {})
        if key in section and section[key] not in (None, ""):
            return section[key]
    except Exception:
        pass
    return os.environ.get(f"HF_{key.upper()}", default)


def _get_hf_token() -> Optional[str]:
    return (
        _hf_setting("token")
        or os.environ.get("HF_TOKEN")
        or os.environ.get("HUGGINGFACE_TOKEN")
        or os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    )


def _strip_thinking(text: str) -> str:
    """Qwen3 models can emit ``<think>...</think>`` chains; strip them."""
    if "</think>" in text:
        text = text.split("</think>", 1)[-1]
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.replace("<think>", "").replace("</think>", "").strip()


@st.cache_resource(show_spinner=False)
def get_client() -> InferenceClient:
    """Build (and cache) the InferenceClient based on secrets."""
    token = _get_hf_token()
    if not token:
        raise RuntimeError(
            "No Hugging Face token configured. Add `[huggingface] token = \"hf_...\"` "
            "to .streamlit/secrets.toml (or set HF_TOKEN in the Streamlit Cloud "
            "secrets pane)."
        )

    endpoint_url = _hf_setting("endpoint_url")
    provider = _hf_setting("provider")
    model_id = _hf_setting("model") or _hf_setting("merged_model") or DEFAULT_MODEL_ID

    kwargs: Dict = {"token": token, "timeout": 120}

    if endpoint_url:
        # Dedicated Inference Endpoint — `model` is the full URL.
        kwargs["model"] = endpoint_url
    else:
        kwargs["model"] = model_id
        if provider:
            kwargs["provider"] = provider

    return InferenceClient(**kwargs)


def _build_messages(user_message: str, history: List[Dict]) -> List[Dict]:
    messages: List[Dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history or []:
        role = msg.get("role")
        content = msg.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    if (
        not messages
        or messages[-1].get("role") != "user"
        or messages[-1].get("content") != user_message
    ):
        messages.append({"role": "user", "content": user_message})
    return messages


def generate_reply(user_message: str, history: List[Dict]) -> str:
    """Call HF and return the assistant reply text."""
    client = get_client()
    messages = _build_messages(user_message, history)

    max_new_tokens = int(_hf_setting("max_new_tokens", 512))
    temperature = float(_hf_setting("temperature", 0.7))
    top_p = float(_hf_setting("top_p", 0.9))

    response = client.chat_completion(
        messages=messages,
        max_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
    )

    text = response.choices[0].message.content or ""
    return _strip_thinking(text) or (
        "I'm here with you. Could you tell me a bit more about what's on your mind?"
    )
