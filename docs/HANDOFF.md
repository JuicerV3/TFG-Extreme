# TFG-Extreme Thai Localization Handoff

**Date:** 2026-08-10
**Repository:** `/Users/tnkrt.nt/Developer/TFG-Extreme`
**MVP branch:** `translate/th_th`
**Full-pass branch:** `feat/localization-th-full`
**Approved MVP PR:** https://github.com/JuicerV3/TFG-Extreme/pull/3
**MVP commit:** `0c73c7e84`

## Mission

Complete Thai (`th_th`) localization using Antigravity/Gemini as the NLP
translator, with GPT orchestration and deterministic structural validation.

This is not permission to build a machine-translation engine. Scripts may parse
source/context, build manifests, compare structure, validate controls, compare
Patchouli links, and report drift. Scripts must not translate prose, construct
Thai sentences, or apply dictionaries/regex replacements to language content.

## Product Rules

- Translate explanations, mechanics, instructions, lore, jokes, and UI prose
  into natural Thai.
- Preserve exact canonical searchable names when actual game context proves they
  are object names.
- Preserve mod names, GT voltage tiers, technical IDs, symbols, units, and
  resource identifiers.
- Resolve overlapping names using the longest exact canonical span.
- Translate ordinary descriptors and concepts when they are not canonical
  object names.
- Preserve Patchouli link targets inside `$(l:...)` byte-for-byte. Visible link
  labels may be translated.
- Preserve Patchouli/FTB/Minecraft controls, placeholders, quantities, and
  structure.
- Never accept fluent output that changes game meaning or searchable names.

## Important Source Locations

- TFG English language source: `kubejs/assets/tfg/lang/en_us.json`
- TFG quest structure/context: `config/ftbquests/quests/chapters/*.snbt`
- FTB Quests English UI: `kubejs/assets/ftbquests/lang/en_us.json`
- TFC English language source: `kubejs/assets/tfc/lang/en_us.json`
- GTCEu English language source: `kubejs/assets/gtceu/lang/en_us.json`
- Other mod language sources: `kubejs/assets/*/lang/en_us.json`
- Field Guide English source: `kubejs/assets/tfc/patchouli_books/field_guide/en_us/`
- Approved Thai MVP: `kubejs/assets/**/th_th/` files already committed on
  `translate/th_th`

## Current Full-Pass Scope

- 90 English `lang/en_us.json` files
- approximately 43,809 localization keys
- 81 Field Guide entry JSON files
- 3 Field Guide category JSON files

Full-pass work is intentionally on `feat/localization-th-full`; do not rewrite
or force-update the approved MVP branch or PR.

## Existing Orchestration Files

- `docs/localization/th_th/README.md`: pilot architecture and review gate
- `docs/localization/th_th/glossary.md`: accepted Thai concept terminology
- `docs/localization/th_th/pilot.json`: pilot keys and canonical-name fixtures
- `docs/localization/th_th/qa.md`: MVP QA findings and human test checklist
- `docs/localization/th_th/translation_batches.md`: agent handoff records
- `docs/localization/th_th/full_pass.md`: full-pass scope and current status
- `tools/validate_th_localization.py`: deterministic validator

## Validator Usage

Validate a flat language batch:

```bash
python3 tools/validate_th_localization.py \
  --manifest docs/localization/th_th/pilot.json \
  --source kubejs/assets/<mod>/lang/en_us.json \
  --translated /tmp/<batch>.json \
  --allow-source-superset
```

Validate Patchouli structure and links:

```bash
python3 tools/validate_th_localization.py \
  --manifest docs/localization/th_th/pilot.json \
  --patchouli-source kubejs/assets/tfc/patchouli_books/field_guide/en_us/<entry>.json \
  --patchouli-translated /tmp/<entry>.json
```

The validator checks JSON shape, placeholders, formatting controls, macro
structure, exact Patchouli link targets, and canonical-name retention. It does
not judge Thai semantics.

## Active Acceptance Target

The current delivery target is intentionally narrower than the original full
pass:

1. Complete the Field Guide: all 81 entries and all 3 categories.
2. Complete FTB Quests through the Primitive Ages, including the relevant Stone
   Age, early metallurgy, and early progression quest chapters referenced by
   the chapter SNBT files.
3. Reach at least 90% rule coverage for the accepted Guide Book and Primitive
   Age quest text before opening the PR.

### Naming Rule Contract

- Keep exact English names for item names, block names, fluids, materials,
  tools, machines, components, armor, recipe outputs, and searchable game
  objects/items.
- Keep mod names, IDs, symbols, units, voltage tiers, and technical notation
  exact, including `mB`, `EU/t`, and `LV`.
- Translate Thai explanations, instructions, verbs, mechanics explanations,
  warnings, progression guidance, jokes, lore, and connective prose.
- Never translate an item or other searchable object merely because it appears
  inside ordinary prose.
- Preserve all Patchouli targets and FTB/Minecraft formatting controls exactly.

### Completion Gates

- Every targeted source key or Field Guide tree has a Thai counterpart.
- Deterministic structure, placeholder, control-token, canonical-name, and
  Patchouli-link validation passes.
- Semantic audit demonstrates at least 90% compliance with the Naming Rule
  Contract for the targeted Guide Book and quests.
- Client and dedicated-server checks pass before PR creation.

## Agent Protocol

Use Herdr only from the managed pane with `HERDR_ENV=1`.

Before every new task sent to an Antigravity pane:

```bash
herdr agent prompt <pane> "/clear" --wait --timeout 120000 || true
```

The slash command commonly reports `agent_prompt_stalled` while leaving the pane
idle. Verify the pane with `herdr agent get <pane>` before sending the next task.

Translation prompts must:

- identify exact source files and bounded keys/entries;
- provide chapter/mod/mechanic context;
- provide glossary and immutable-name rules;
- require direct NLP translation only;
- forbid scripts, dictionaries, repository edits, and generated translation;
- require output to `/tmp/<batch>.json` and reply with only the path;
- require `__review__` for ambiguity.

Do not merge an agent output directly. Read it, run the validator, inspect
semantics, and regenerate rejected batches.

## Completed Full-Pass Waves

- Stone Age quest subset: structurally passed; semantic review still required.
- Food and Water Field Guide: structurally passed; semantic review still
  required.
- Direct TFC UI subset: passed.
- GTCEu behavior subset: one key regenerated because `Create` was dropped.
- Direct TFG UI subset: regenerated after a broad batch translated canonical
  names; direct subset passed.
- TFC command UI subset: passed.
- GTCEu prospector subset: passed.
- Metallurgy quest subset: passed.
- TFG ore tooltip subset: regenerated/focused; passed structurally.

## Rejected Output Lessons

- Broad TFG UI output translated canonical names such as `Copper`, `Tin`, and
  `Javelin`; do not accept it.
- `building_materials.json` dropped `Thatch`, `Stone Knife`, and `Straw`.
- `anvils.json` dropped canonical alloy/material names and changed one page's
  JSON keys.
- Regeneration of both `building_materials.json` and `anvils.json` still fails
  exact JSON-key comparison; keep both outputs rejected.
- One agent attempted to generate translation scripts; discard that output.
- `$(t:...)` contains visible tooltip prose. Its wrapper must remain intact,
  but the text argument may be translated. The validator normalizes this macro
  while checking its structure.

## Work Packages

### WP-01: TFG Quest Chapters

Translate all quest keys referenced by each chapter SNBT in coherent progression
order. Start with `questsstoneage.snbt`, `questsmetallurgy.snbt`,
`questssteam_age.snbt`, and `queststfc_tips.snbt`, then continue through GTCEu,
Create, AE2, space, and advanced chapters. Preserve quest placeholders and
descriptions while using chapter context and dependency order.

### WP-02: TFC Core Language

Partition `kubejs/assets/tfc/lang/en_us.json` by namespace and function. Handle
survival status, commands, tooltips, block interactions, field-guide references,
and UI messages separately. Do not translate material/item/block display names
without actual registry/display-name evidence.

### WP-03: GTCEu Language

Partition `kubejs/assets/gtceu/lang/en_us.json` by behavior, prospector/tool
messages, machines, materials, recipes, voltage tiers, and UI. Keep material
names, machine names, tiers, EU/t, mB, A, V, and recipe terminology exact where
they are searchable or symbolic.

### WP-04: Field Guide

Translate all 81 entry JSON files and 3 categories in coherent sections:
getting_started, mechanics, tfg_ores, tfg_tips, firmalife, Beneath, space,
transport, and integrations. Every output must be structure-compared against
the English source and every `$(l:...)` target must match exactly.

### WP-05: Mod UI and Integration Lang

Translate remaining mod language files in coherent mod batches. Prioritize
player-facing UI, tooltips, guide text, questbook strings, and integration
messages. Defer debug/admin-only text unless required for complete locale key
coverage. Never translate resource IDs or canonical display names by pattern.

### WP-06: Cross-Batch Terminology and QA

Maintain the glossary for gameplay concepts only. Audit accepted batches for
canonical-name drift, Thai terminology drift, placeholder/control loss, link
target changes, and source drift. Record ambiguous strings and rejected batches.

### WP-07: Locale Assembly

After semantic acceptance, merge batch JSON into the correct `th_th` paths while
preserving source key ordering where practical. Never overwrite unrelated user
changes. Run key parity and source-drift checks before committing.

### WP-08: Runtime Verification

Run client startup and dedicated-server startup after a meaningful batch group.
Check logs for JSON/KubeJS/Patchouli errors. In-game verify Thai rendering,
Patchouli navigation, EMI/JEI searchability, recipe visibility, placeholders,
line wrapping, and multiplayer-safe behavior.

## Branch and PR Policy

- Keep PR #3 as the approved MVP reference.
- Full-pass work belongs on `feat/localization-th-full` or a clearly named
  follow-up branch.
- Do not force-push shared branches.
- Do not merge full-pass output until structural and semantic QA passes.
- Create a separate full-pass PR after a meaningful validated slice, not after
  blindly generating all keys.

## Next Action

Continue with bounded translation waves on the six idle Antigravity panes. Do
not retry `building_materials.json` without preserving exact source structure.
The accepted assembly currently contains 1,057 flat Thai keys and 75 Field Guide
entries plus all 3 categories, with zero deterministic validation errors. Keep
the six remaining rejected Field Guide outputs out of locale files until
regenerated.

## Latest Resume Blocker

The managed Antigravity pane is currently quota-blocked again. Current assembly
is 1,622 flat
Thai keys and 81 of 81 Field Guide entries. Primitive Stone Age, Metallurgy, and
TFC Tips quest batches are assembled and validated, with 602/602 referenced
Primitive Age keys present. The targeted canonical-name audit is 140/140 and
the complete Guide Book tree audit is clean. Proceed to final runtime checks and
PR preparation; do not replace
NLP translation with scripts, dictionaries, regex translation, or guessed prose.
