import tempfile
import unittest
from pathlib import Path
from src.engine import Event, PolicyViolation, validate_event
from src.audit import append_event, verify_chain

BASE = dict(opportunity_id="DEMO-1", from_stage="Asignado", to_stage="Contacto",
            source_ref="demo://source", owner="demo", next_action="schedule",
            event_timestamp="2026-11-03T12:00:00-06:00", evidence="simulated",
            actor="tester", consent_checked=True)

class PipelineTests(unittest.TestCase):
    def test_valid_transition(self):
        self.assertTrue(validate_event(Event(**BASE))["accepted"])
    def test_cannot_skip_stage(self):
        with self.assertRaises(PolicyViolation):
            validate_event(Event(**{**BASE, "to_stage": "Presentación"}))
    def test_review_required(self):
        with self.assertRaises(PolicyViolation):
            validate_event(Event(**{**BASE, "consent_checked": False}))
    def test_won_needs_approval(self):
        with self.assertRaises(PolicyViolation):
            validate_event(Event(**{**BASE, "from_stage": "Promesa cierre", "to_stage": "Ganado"}))
    def test_audit_tamper_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "events.jsonl")
            append_event(path, {"event": "created"})
            append_event(path, {"event": "updated"})
            self.assertTrue(verify_chain(path))
            f = Path(path)
            f.write_text(f.read_text().replace("updated", "altered"))
            self.assertFalse(verify_chain(path))

if __name__ == "__main__":
    unittest.main()
