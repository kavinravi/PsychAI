#!/usr/bin/env python
"""
Create (or update) a dedicated HF Inference Endpoint for the merged PsychAI
model and write the resulting URL back into website/.streamlit/secrets.toml.

Defaults:
  - repo:        kavin-ravi/qwen3-8b-psychai-merged
  - hardware:    AWS us-east-1, single NVIDIA L4 (24 GB) — fits Qwen3-8B in bf16
  - container:   HF's TGI (Text Generation Inference, OpenAI-compatible /v1/chat)
  - scaling:     min=0 max=1, scale-to-zero after 15 min idle
  - access:      "protected" (token-gated) — same HF token the Streamlit app uses

Run:
    python scripts/create_endpoint.py --token hf_xxx
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict


def _load_token_from_secrets() -> str | None:
    secrets_path = Path(__file__).resolve().parent.parent / "website" / ".streamlit" / "secrets.toml"
    if not secrets_path.exists():
        return None
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib  # type: ignore
        with secrets_path.open("rb") as f:
            return tomllib.load(f).get("huggingface", {}).get("token")
    except Exception:
        return None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", default="psychai-qwen3-8b", help="Endpoint name. Default: %(default)s")
    p.add_argument("--repo", default="kavin-ravi/qwen3-8b-psychai-merged")
    p.add_argument("--region", default="us-east-1")
    p.add_argument("--vendor", default="aws", choices=["aws", "azure", "gcp"])
    p.add_argument("--instance-type", default="nvidia-l4", help="e.g. nvidia-l4, nvidia-a10g, nvidia-l40s")
    p.add_argument("--instance-size", default="x1")
    p.add_argument("--type", default="protected", choices=["public", "protected", "private"])
    p.add_argument("--min-replica", type=int, default=0)
    p.add_argument("--max-replica", type=int, default=1)
    p.add_argument("--scale-to-zero-min", type=int, default=15)
    p.add_argument(
        "--quantize",
        default="fp8",
        choices=["", "eetq", "bitsandbytes", "bitsandbytes-nf4", "bitsandbytes-fp4", "fp8", "awq"],
        help="TGI runtime quantization. fp8 keeps near-bf16 quality and fits under the 30GB host RAM cap on x1 instances.",
    )
    p.add_argument("--max-input-length", type=int, default=3072)
    p.add_argument("--max-total-tokens", type=int, default=4096)
    p.add_argument("--token", default=None, help="HF token (write+inference-endpoints). Falls back to secrets.toml then HF_TOKEN.")
    p.add_argument("--no-wait", action="store_true", help="Don't block until the endpoint is running.")
    p.add_argument("--no-update-secrets", action="store_true")
    return p.parse_args()


def _update_secrets_url(url: str) -> Path:
    secrets_path = Path(__file__).resolve().parent.parent / "website" / ".streamlit" / "secrets.toml"
    text = secrets_path.read_text()
    # Replace existing endpoint_url line (commented or not) or add one under [huggingface]
    if re.search(r"^\s*#?\s*endpoint_url\s*=", text, flags=re.MULTILINE):
        text = re.sub(
            r"^\s*#?\s*endpoint_url\s*=.*$",
            f'endpoint_url = "{url}"',
            text,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        text = re.sub(
            r"(\[huggingface\][^\[]*?)(\n\[|\Z)",
            lambda m: m.group(1).rstrip() + f'\nendpoint_url = "{url}"\n' + (m.group(2) or ""),
            text,
            count=1,
            flags=re.DOTALL,
        )
    secrets_path.write_text(text)
    return secrets_path


def main() -> int:
    args = parse_args()
    token = args.token or os.environ.get("HF_TOKEN") or _load_token_from_secrets()
    if not token:
        print("ERROR: no HF token provided.")
        return 2

    from huggingface_hub import create_inference_endpoint, get_inference_endpoint
    from huggingface_hub.utils import HfHubHTTPError

    # Try to find an existing endpoint with the same name first.
    try:
        ep = get_inference_endpoint(args.name, token=token)
        print(f"[info] found existing endpoint {args.name!r} (status={ep.status})")
    except HfHubHTTPError:
        ep = None

    if ep is None:
        print(f"[info] creating endpoint {args.name!r} for {args.repo}")
        print(f"       hardware: {args.vendor}/{args.region} {args.instance_type} {args.instance_size}")
        print(f"       scaling : min={args.min_replica} max={args.max_replica} (scale-to-zero after {args.scale_to_zero_min} min idle)")
        # Explicitly pin TGI; HF's default image for this repo is the slow
        # transformers-based inference toolkit which (a) ignores QUANTIZE and
        # (b) peaks RAM during shard loading. TGI streams weights and respects
        # quantization. MODEL_ID must be set or TGI falls back to bloom-560m.
        env: Dict[str, str] = {
            "MODEL_ID": args.repo,
            "REVISION": "main",
            "MAX_INPUT_LENGTH": str(args.max_input_length),
            "MAX_TOTAL_TOKENS": str(args.max_total_tokens),
            "MAX_BATCH_PREFILL_TOKENS": str(args.max_input_length + 256),
            "HF_HUB_ENABLE_HF_TRANSFER": "1",
            # The TGI image's base locale is plain "C", which makes Python's
            # tokenizer loader choke on any non-ASCII byte in tokenizer_config
            # (em-dashes / curly quotes in the Qwen3 chat template). When that
            # happens TGI silently falls back to "legacy" tokenization which
            # has no chat template support → /v1/chat/completions returns 500.
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONIOENCODING": "utf-8",
        }
        if args.quantize:
            env["QUANTIZE"] = args.quantize
        # Token for TGI to download the (protected) model from the Hub.
        secrets = {"HUGGING_FACE_HUB_TOKEN": token, "HF_TOKEN": token}
        try:
            ep = create_inference_endpoint(
                name=args.name,
                repository=args.repo,
                framework="pytorch",
                task="text-generation",
                accelerator="gpu",
                vendor=args.vendor,
                region=args.region,
                instance_type=args.instance_type,
                instance_size=args.instance_size,
                type=args.type,
                min_replica=args.min_replica,
                max_replica=args.max_replica,
                scale_to_zero_timeout=args.scale_to_zero_min,
                custom_image={
                    "url": "ghcr.io/huggingface/text-generation-inference:3.3.6",
                },
                env=env,
                secrets=secrets,
                token=token,
            )
        except HfHubHTTPError as e:
            print(f"\nERROR creating endpoint: {e}")
            print("\nCommon causes:")
            print("  * No payment method on your HF account — add one at https://huggingface.co/settings/billing")
            print("  * Token missing 'manage Inference Endpoints' scope (classic write tokens have it; fine-grained may not)")
            print("  * Out-of-quota for that GPU type/region — try a different region or instance_type")
            return 3

    print(f"[info] endpoint URL (may be inactive until status=running): {ep.url}")

    if not args.no_wait:
        print("[info] waiting for endpoint to reach 'running' (this typically takes 3–8 min)…")
        last_status = None
        deadline = time.time() + 20 * 60
        while time.time() < deadline:
            ep.fetch()
            if ep.status != last_status:
                print(f"  status: {ep.status}")
                last_status = ep.status
            if ep.status == "running":
                break
            if ep.status in ("failed", "scaledToZero"):
                # scaledToZero shouldn't happen on first deploy, but if it does it still has a URL
                if ep.status == "failed":
                    print("ERROR: endpoint deployment failed. Check the HF UI for logs.")
                    return 4
                break
            time.sleep(15)
        else:
            print("WARN: timed out waiting; check https://ui.endpoints.huggingface.co/")

    print(f"[info] final URL: {ep.url}")

    if not args.no_update_secrets:
        path = _update_secrets_url(ep.url)
        print(f"[info] wrote endpoint_url into {path}")

    print("\n[done] endpoint is ready. Test it with:")
    print(f"  python scripts/test_endpoint.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
