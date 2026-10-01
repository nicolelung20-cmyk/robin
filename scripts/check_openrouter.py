"""Check OpenRouter access: key works, model exists, one short completion.

Usage: OPENROUTER_API_KEY=... python scripts/check_openrouter.py [model]
The key is read from the environment only. Exits non-zero on any failure.
"""
import os
import sys

import requests

BASE = os.environ.get("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "openai/gpt-4o-mini"
KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
if not KEY:
    sys.exit("OPENROUTER_API_KEY is not set")

head = {"Authorization": f"Bearer {KEY}"}
ids = {m["id"] for m in requests.get(f"{BASE}/models", headers=head, timeout=30).json()["data"]}
print(f"{len(ids)} models listed; {MODEL!r} present: {MODEL in ids}")
if MODEL not in ids:
    sys.exit(f"model {MODEL!r} is not on OpenRouter")

r = requests.post(f"{BASE}/chat/completions", headers=head, timeout=60, json={
    "model": MODEL, "max_tokens": 20,
    "messages": [{"role": "user", "content": "Reply with the word ok."}]})
r.raise_for_status()
print("reply:", r.json()["choices"][0]["message"]["content"])
