# Thai Full-Pass Orchestration

This is the follow-up to the approved MVP in PR #3. The MVP remains the first
human-reviewable slice; full-pass work is being performed on a separate branch.

## Scope Snapshot

- 90 English `lang/en_us.json` files
- approximately 43,809 localization keys
- 81 Field Guide entry JSON files
- 3 Field Guide category JSON files

The English source remains authoritative. Translation agents receive bounded
source batches with context and return locale content only. No script may
translate prose or construct Thai sentences.

## Batch Rules

- Keep batches coherent by mod, chapter, or Field Guide section.
- Keep each agent response bounded enough for semantic review.
- Preserve canonical display names only when supported by actual source/game
  data; use longest exact match for overlaps.
- Preserve Patchouli link targets exactly; visible link labels may be Thai.
- Validate every batch before merging it into the locale tree.
- Record ambiguous strings instead of guessing.

## Initial Dispatch

- Stone Age and early metallurgy quest references
- Remaining early-game Field Guide entries
- TFC UI and survival terminology
- GTCEu prospecting and tool behavior
- TFG-owned non-quest strings
- TFC Field Guide mechanics/prospecting entries

This dispatch starts the full pass. It does not authorize automatic acceptance
of agent output or skip human review of high-risk technical sections.

## Narrowed Delivery Target

The active delivery target is complete Field Guide coverage plus Primitive Age
FTB Quests, with at least 90% compliance against the naming contract recorded in
`docs/HANDOFF.md`. Broader flat-locale work is secondary until those gates pass.

## Dispatch Status

The first two waves have been sent through six Antigravity panes. Outputs are
held in temporary batch files until review:

- Passed structure: Stone Age quests, Food and Water, direct TFC UI, GTCEu
  prospector behavior, TFC command UI, metallurgy quest subset, and TFG ore
  tooltip subset.
- Regenerated and passed: direct TFG UI subset and GTCEu canoe tooltip.
- Rejected: broad generated TFG UI output, because canonical names were
  translated; `building_materials.json`, because canonical names were dropped;
  `anvils.json`, because canonical names were dropped and one page structure
  changed.
- Pending focused review: mechanics prospecting/support-beams output.

Structural passage is not semantic acceptance. Accepted batches still require
orchestrator meaning review before they enter `th_th` locale files.

## Current Assembly Status

- Full-pass branch: `feat/localization-th-full`.
- Flat Thai locale assembly: 1,622 of approximately 43,809 source keys across
  the TFG, FTB Quests, and GTCEu locale files; accepted assembled files pass
  the deterministic validator.
- Field Guide assembly: 81 of 81 entries and all 3 category files are present
  in `th_th` and pass structure, control-token, and Patchouli-link validation.
- The latest valid batches were assembled only after validation. All 81 Field
  Guide entries and all 3 categories now pass the full tree validator.
- Primitive Stone Age quest coverage is assembled and passes validation. The
  Primitive Metallurgy and TFC Tips batches are now assembled and pass focused
  formatting-control validation after correction batches.
- Primitive Age quest audit: 602 of 602 keys referenced by
  `questsstoneage.snbt`, `questsmetallurgy.snbt`, and `queststfc_tips.snbt` are
  present in the Thai TFG locale.
- Naming-rule audit: 140 of 140 canonical-name occurrence checks pass across
  the targeted Primitive Age quest text; Guide Book tree validation reports no
  canonical-name or control-token failures.
- The prior Antigravity/Gemini pane exhausted its individual quota. Four fresh
  OpenCode panes are available for the narrowed delivery target; use Herdr and
  issue `/clear` before each new request.

## Resume Queue

1. Run the final targeted client/server or pack-load checks that are available.
2. Review the diff for unrelated/generated files and prepare the narrowed PR.
3. Broader flat-language work remains optional and must not block the narrowed
   Primitive Age plus complete Guide Book delivery.
