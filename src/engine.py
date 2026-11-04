"""Deterministic offline AXIA stage validator. No network or real customer data."""
import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

CONFIG = json.loads((Path(__file__).resolve().parents[1] / "config" / "pipeline.json").read_text(encoding="utf-8"))

class PolicyViolation(ValueError):
    pass

@dataclass(frozen=True)
class Event:
    opportunity_id: str
    from_stage: str
    to_stage: str
    source_ref: str
    owner: str
    next_action: str
    event_timestamp: str
    evidence: str
    actor: str
    consent_checked: bool = False
    approval_id: str = ""

def validate_event(event: Event) -> dict:
    stages = CONFIG["stages"]
    if event.from_stage not in stages:
        raise PolicyViolation("Active source stage required")
    if event.to_stage not in stages + CONFIG["terminal_outcomes"]:
        raise PolicyViolation("Unknown destination")
    idx = stages.index(event.from_stage)
    if event.to_stage in stages and stages.index(event.to_stage) != idx + 1:
        raise PolicyViolation("Exception workflow required for skipping/regression")
    if event.to_stage == "Ganado" and event.from_stage != "Promesa cierre":
        raise PolicyViolation("Winning transition requires final active stage")
    for key in ("opportunity_id", "source_ref", "owner", "next_action", "event_timestamp", "evidence", "actor"):
        value = getattr(event, key)
        if not isinstance(value, str) or not value.strip():
            raise PolicyViolation("Missing field: " + key)
    try:
        stamp = datetime.fromisoformat(event.event_timestamp.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError()
    except ValueError:
        raise PolicyViolation("Timezone-aware timestamp required") from None
    if not event.consent_checked:
        raise PolicyViolation("Privacy review not confirmed")
    if event.to_stage == "Ganado" and not event.approval_id.strip():
        raise PolicyViolation("Approval reference required")
    return {"accepted": True, "opportunity_id": event.opportunity_id, "stage": event.to_stage, "evidence_ref": event.source_ref}

def demo():
    event = Event("DEMO-001", "Asignado", "Contacto", "demo://interaction/1", "demo-owner",
                  "Schedule demo", datetime.now(timezone.utc).isoformat(), "Simulated interaction", "demo-actor", True)
    print(json.dumps(validate_event(event), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        parser.print_help()
