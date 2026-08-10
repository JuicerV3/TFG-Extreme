# Pilot QA

## Orchestrator Findings

- Quest output was regenerated after the first pass preserved a non-canonical
  `Stone Axe` in an axe-head task and used awkward pickaxe wording.
- A Patchouli pass dropped `$(k:key.use)` from a control expression. The pilot
  was rejected until the exact macro was restored.
- A guide pass mistranslated “voila” as `แล้ววัวล่า!`; it was corrected to a
  natural Thai completion phrase.
- Canonical audit removed generic concepts such as `Workbench`, `Lumber`,
  `Clay`, `Field Guide`, and generic clothing from the immutable-name list.
- Prefix cases are represented in `pilot.json`; longest canonical spans remain
  the required resolution rule.

## Deterministic Checks

The following checks pass:

- all pilot locale JSON files parse;
- FTB Quests and quest pilot keys retain placeholders and formatting codes;
- all three translated Patchouli entries retain nested JSON structure, IDs,
  links, macros, quantities, and canonical names;
- manifest metadata validates.

## Human/In-Game Gate

Not yet completed. A Thai-speaking reviewer must check:

- quest titles, descriptions, and humor in the Stone Age chapter;
- EMI search using each retained object name, especially `Stone Knife`,
  `Stone Axe`, `Small Vessel`, `Pit Kiln`, `Copper`, and alloy names;
- Patchouli navigation, visible links, recipe previews, images, and macros;
- FTB Quests UI line wrapping and parameter substitution;
- Thai font rendering and mobile/low-resolution readability where applicable.

Bulk translation must not begin until this gate is approved.
