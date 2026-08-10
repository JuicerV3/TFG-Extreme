# Translation Batches

## Batch Contract

Antigravity/Gemini receives source text and repository-derived context. It must
return only translated key/value content, with no file edits, key renames, or
automatic translation machinery.

Required translator behavior:

> Translate into fluent natural Thai. Preserve every canonical game-object name
> marked immutable as an atomic English noun phrase. Translate concepts and
> ordinary descriptors naturally. Preserve control syntax, quantities, links,
> line breaks, and technical meaning. Do not invent mechanics or names. Mark
> genuine ambiguity for orchestrator review.

## Handoff Records

Agent responses are recorded after the orchestrator reviews them. A response is
not accepted merely because it is fluent: semantic, canonical-name, prefix, and
formatting QA are required first.

## Current Batches

- `stone-age-quests`: translated, regenerated, and accepted after orchestrator QA
- `field-guide-getting-started`: three entries translated and structurally accepted;
  semantic corrections recorded in `qa.md`
- `ftbquests-ui`: translated and structurally accepted

## Agent Handoff Notes

Six idle Antigravity panes were used through Herdr. Three performed bounded NLP
translation and three independently audited canonical names, terminology, and
structure. Each new task was preceded by a `/clear` handoff attempt. Herdr
reported the slash command as stalled because Antigravity emitted no lifecycle
transition, but all panes were verified idle before the next prompt.
