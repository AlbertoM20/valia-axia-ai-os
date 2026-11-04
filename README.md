# VALIA / AXIA AI Operating System

**Public source-code prototype — v0.2 (not deployed).** Synthetic data only.

This repository contains an offline, deterministic commercial pipeline validator and illustrative tamper-detection audit log. It does **not** connect to CRM, Notion, Plaud, banking, payroll, or messaging systems, and is not an autonomous agent.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 -m src.engine --demo
```

## Scope and safety

- Pipeline demo: Asignado > Contacto > Agenda > Presentación > Dudas técnicas > Promesa cierre; Ganado/Perdido are terminal outcomes.
- Every transition needs an owner, evidence reference, time and next action. Human privacy review is required; this marker does **not** establish legal consent.
- Ganado requires an approval reference. **No emails, payments, contracts, credit decisions, or external API calls.**
- The hash chain is illustrative, not an immutable ledger.
- Never commit real customer/investor/employee information, credentials, call recordings, business strategies, contracts, or production configuration.
- Production connectors, security governance, persistence, monitoring and approval execution remain unimplemented.
- No DNS or hosting required for this local demonstration.

## Gate to production

First validate source-of-truth, access boundaries, data-processing authority, versioned schemas, idempotent tasks, real approval enforcement, audit retention and a baseline for incremental commercial outcomes.

This open-source skeleton should not be confused with a working AI operating system.
