"""Local hash chain demo. Not tamper-proof; do not put private data in logs."""
import hashlib
import json
from pathlib import Path

def digest(prev, payload):
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256((prev + canonical).encode("utf-8")).hexdigest()

def append_event(path: str, payload: dict) -> str:
    target = Path(path)
    prev = "GENESIS"
    if target.exists():
        rows = target.read_text(encoding="utf-8").splitlines()
        if rows:
            prev = json.loads(rows[-1])["hash"]
    result = digest(prev, payload)
    with target.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"previous_hash": prev, "payload": payload, "hash": result}, ensure_ascii=False) + "\n")
    return result

def verify_chain(path: str) -> bool:
    prev = "GENESIS"
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if item["previous_hash"] != prev or item["hash"] != digest(prev, item["payload"]):
            return False
        prev = item["hash"]
    return True
