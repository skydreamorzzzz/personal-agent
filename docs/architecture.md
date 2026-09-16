# Personal Agent Architecture v0.1

## Purpose

Personal Agent is designed as a stateful personal-agent runtime. LangGraph is the
control plane for state transitions; it is not the capability implementation and
the LLM is not the owner of irreversible actions.

## Five layers

1. **Entry / UI** accepts user input, confirmations, or external events.
2. **Runtime / Control Plane** owns state, nodes, edges, routing, interruption,
   checkpoint integration, and finalization.
3. **Capabilities** describe what the system can do for filesystem, personal
   data, mail, and ehall. They may later be tools, services, nodes, or subgraphs.
4. **Human-in-the-loop** owns approve, reject, edit, and clarification decisions.
5. **Persistence / Knowledge / Memory / Skills / Observability** stores durable
   concepts and explains what happened.

The graph decides workflow. A capability performs a bounded operation. A
capability must not decide the overall workflow, and a capability is not required
to map one-to-one to a graph node.

## State, context, and durable concepts

`AgentState` contains only task-changing information: messages, task, artifacts,
pending action, and status. `RuntimeContext` contains process dependencies such as
model configuration, workspace path, checkpoint backend, memory backend,
capability registry, and logger. It is not graph state.

- **Checkpoint**: where the current task is paused or executing.
- **Knowledge**: the user's source material, with provenance and original paths.
- **Memory**: cross-task information, initially `profile`, `rules`, and `episodes`.
- **Skills**: reusable successful workflows and procedures; separate from memory.
- **Journal**: human-readable, version-controlled project evolution.
- **Log**: machine-generated execution and debugging records.

Canonical memory should remain human-readable and Git-diffable. Semantic indexes,
vector indexes, or LangGraph Store entries are derived runtime data, not the only
source of truth.

## Side-effect safety

Any irreversible operation follows:

`ActionProposal -> Approval -> Execute`

An LLM may propose an action, but it does not directly own the permission to send
mail, submit a form, delete a file, archive mail, or modify remote data. Approval
will later use LangGraph interrupt/resume semantics.

## Hybrid memory

The first architecture includes three deliberately asymmetric paths:

- `memory_retrieve` runs before task work.
- Explicit user facts, corrections, preferences, and rules may update memory on
  the hot path through `memory_write`.
- Ordinary implicit preferences and episode observations go through the separate
  `memory_reflection` node after finalization.

Weak inference must not silently become long-term memory. Skills remain a separate
concept even when a workflow is learned from an episode.

## Current scope

The repository currently contains a real graph builder and typed domain/state
shapes. Nodes, capabilities, persistence, human approval, memory backends,
observability, and the LLM adapter are scaffolds or placeholders. No external API,
mail, ehall, browser, or irreversible operation is connected.
