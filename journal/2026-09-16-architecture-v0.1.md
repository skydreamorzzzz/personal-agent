# Architecture v0.1

## Context

The previous handwritten ReAct prototype has been archived as
`handwritten-react-v1`. The project is being rebuilt on LangGraph so the workflow,
pause/resume boundaries, and side-effect policy are explicit before business
capabilities are implemented.

## Goals

- Build a personal agent for GSE Lab1.
- Work architecture-first and implement capabilities incrementally.
- Keep the runtime understandable, inspectable, and safe by default.

## Decisions

- Use five layers: Entry/UI, LangGraph Runtime, Capabilities, Human-in-the-loop,
  and Persistence/Knowledge/Memory/Skills/Observability.
- Use LangGraph as the runtime/control plane, not as a capability implementation.
- Keep Graph and Capability responsibilities separate.
- Use asymmetric hybrid memory: retrieve before tasks, explicit hot-path writes,
  and post-task reflection.
- Require `ActionProposal -> Approval -> Execute` for side effects.
- Keep canonical memory human-readable and version-controllable.
- Keep Checkpoint, Knowledge, Memory, and Skills separate.
- Keep machine Log and human Journal separate.

## Current Reality

- **Implemented:** typed domain/state shapes, runtime context shape, StateGraph
  builder, named node registration, conditional routing, documentation, and
  journal conventions.
- **Scaffolded:** capability protocol/registry, human approval boundary,
  persistence interfaces, memory interfaces, LLM boundary, and logger boundary.
- **Placeholder:** all graph nodes that would call an external model, tool,
  database, mail system, ehall, browser, or memory backend.
- **Unavailable:** real capabilities, checkpoint persistence, memory retrieval or
  reflection, human interrupt/resume, and external side effects.

## Open Questions

- Which StateGraph and checkpoint contracts should be frozen after review?
- What is the first safe filesystem capability and its approval policy?
- Which canonical memory file layout best supports edits and provenance?
- How should runtime logs be redacted before any production use?

## Next Review

The next step is an Architecture Review, not immediate feature implementation.
