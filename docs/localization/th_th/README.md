# Thai Localization Pilot

This directory contains the bounded `th_th` pilot for TFG-Extreme. It is an
orchestration and review artifact, not a machine-translation pipeline.

## Scope

- Stone Age / Early TFC: 24 quest keys covering titles, jokes, long prose,
  mechanics, numbers, formatting, and searchable objects.
- TFC Field Guide: `getting_started/introduction.json`,
  `getting_started/finding_ores.json`, and
  `getting_started/primitive_alloys.json`.
- FTB Quests UI: 8 representative labels/messages with parameters and line
  breaks.

Translation is performed by Antigravity/Gemini from context-rich batches. The
orchestrator reviews meaning, exact object names, prefixes, Thai fluency, and
formatting before accepting output.

## Review Gate

The pilot must pass `python3 tools/validate_th_localization.py` and GPT semantic
QA before a human checks it in-game. Bulk translation is explicitly out of
scope until that review is approved.

## Files

- `glossary.md`: authoritative Thai terms for gameplay concepts.
- `pilot.json`: source keys, contexts, canonical names, and pilot coverage.
- `translation_batches.md`: bounded prompts and agent handoff records.
- `qa.md`: acceptance findings and human/in-game QA checklist.
