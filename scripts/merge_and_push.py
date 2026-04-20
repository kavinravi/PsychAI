#!/usr/bin/env python
"""
Merge the PsychAI LoRA adapter into Qwen3-8B and push the resulting standalone
model to the Hugging Face Hub.

Run this ONCE on a machine with the base model + CUDA torch (your training box
already has both). After it finishes, the new repo
`kavin-ravi/qwen3-8b-psychai-merged` will be a normal causal LM that any HF
Inference Provider can serve — no PEFT, no adapters, no LoRA loading at runtime.

Usage:
    # Pick up token from website/.streamlit/secrets.toml (default), env, or CLI.
    python scripts/merge_and_push.py

    # Or override anything:
    python scripts/merge_and_push.py \\
        --base ~/CodingStuff/models/qwen3-8b \\
        --adapter kavin-ravi/qwen3-8b-psychai-lora \\
        --target kavin-ravi/qwen3-8b-psychai-merged \\
        --token hf_xxx
"""

from __future__ import annotations

import argparse
import gc
import os
import sys
from pathlib import Path


def _load_token_from_secrets() -> str | None:
    secrets_path = Path(__file__).resolve().parent.parent / "website" / ".streamlit" / "secrets.toml"
    if not secrets_path.exists():
        return None
    try:
        try:
            import tomllib  # py3.11+
        except ImportError:
            import tomli as tomllib  # type: ignore
        with secrets_path.open("rb") as f:
            data = tomllib.load(f)
        return data.get("huggingface", {}).get("token")
    except Exception as e:
        print(f"[warn] couldn't read {secrets_path}: {e}")
        return None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--base",
        default=os.path.expanduser("~/CodingStuff/models/qwen3-8b"),
        help="Path or HF id of the base model. Default: %(default)s",
    )
    p.add_argument(
        "--adapter",
        default="kavin-ravi/qwen3-8b-psychai-lora",
        help="HF id (or local path) of the LoRA adapter. Default: %(default)s",
    )
    p.add_argument(
        "--target",
        default="kavin-ravi/qwen3-8b-psychai-merged",
        help="HF repo id to push the merged model to. Default: %(default)s",
    )
    p.add_argument(
        "--out-dir",
        default="merged-psychai",
        help="Local scratch dir for the merged weights. Default: %(default)s",
    )
    p.add_argument(
        "--token",
        default=None,
        help="HF token (write scope). Falls back to secrets.toml then HF_TOKEN env.",
    )
    p.add_argument(
        "--private",
        action="store_true",
        help="Push as a private repo. Default: public (matches the LoRA repo).",
    )
    p.add_argument(
        "--dtype",
        default="bfloat16",
        choices=["bfloat16", "float16", "float32"],
        help="Save dtype. bfloat16 is recommended for Qwen3.",
    )
    p.add_argument(
        "--no-push",
        action="store_true",
        help="Only merge + save locally, don't upload to the Hub.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    token = args.token or os.environ.get("HF_TOKEN") or _load_token_from_secrets()
    if not token and not args.no_push:
        print("ERROR: no HF token. Pass --token, set HF_TOKEN, or fill in website/.streamlit/secrets.toml.")
        return 2

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    dtype = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}[args.dtype]
    device_map = "auto" if torch.cuda.is_available() else "cpu"
    print(f"[info] loading base model: {args.base}  (dtype={args.dtype}, device_map={device_map})")

    base = AutoModelForCausalLM.from_pretrained(
        args.base,
        torch_dtype=dtype,
        device_map=device_map,
        low_cpu_mem_usage=True,
        token=token,
    )

    print(f"[info] loading tokenizer from adapter repo: {args.adapter}")
    tokenizer = AutoTokenizer.from_pretrained(args.adapter, token=token)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"[info] attaching LoRA adapter: {args.adapter}")
    model = PeftModel.from_pretrained(base, args.adapter, token=token)

    print("[info] merging adapter into base weights (merge_and_unload)…")
    model = model.merge_and_unload()
    model.eval()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[info] saving merged model to {out_dir}")
    model.save_pretrained(out_dir, safe_serialization=True, max_shard_size="4GB")
    tokenizer.save_pretrained(out_dir)

    del model, base
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if args.no_push:
        print(f"[done] merged model saved locally at {out_dir}. Skipping push.")
        return 0

    print(f"[info] pushing to Hub repo: {args.target}  (private={args.private})")
    from huggingface_hub import HfApi, create_repo

    create_repo(args.target, token=token, exist_ok=True, private=args.private, repo_type="model")

    api = HfApi(token=token)
    api.upload_folder(
        repo_id=args.target,
        folder_path=str(out_dir),
        repo_type="model",
        commit_message="Upload merged PsychAI (Qwen3-8B + LoRA) model",
    )

    _write_model_card(api, args)

    print(f"[done] https://huggingface.co/{args.target}")
    return 0


def _write_model_card(api, args) -> None:
    card = f"""---
license: apache-2.0
base_model: Qwen/Qwen3-8B
tags:
  - text-generation
  - conversational
  - mental-health
  - psychai
  - merged
pipeline_tag: text-generation
---

# PsychAI — Qwen3-8B (LoRA merged)

This is `{args.adapter}` merged into `Qwen/Qwen3-8B`, so it can be served by any
standard inference provider without needing to load PEFT adapters at runtime.

It's intended for serverless inference (HF Inference Providers / dedicated
Inference Endpoints) by the PsychAI Streamlit app.

## Intended use

Empathetic, age-appropriate conversational support for teens dealing with
anxiety, mood dips, and everyday stressors. **Not** a substitute for licensed
mental-health care. If you or someone you know is in crisis, contact your local
emergency services or call/text **988** (US Suicide & Crisis Lifeline).

## Quick start

```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="{args.target}", token="hf_***")
out = client.chat_completion(
    messages=[
        {{"role": "system", "content": "You are PsychAI..."}},
        {{"role": "user", "content": "I've been feeling anxious lately."}},
    ],
    max_tokens=512, temperature=0.7, top_p=0.9,
)
print(out.choices[0].message.content)
```
"""
    api.upload_file(
        path_or_fileobj=card.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=args.target,
        repo_type="model",
        commit_message="Add model card",
    )


if __name__ == "__main__":
    sys.exit(main())
