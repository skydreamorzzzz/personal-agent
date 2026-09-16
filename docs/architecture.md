# Personal Agent Architecture v0.1

## Purpose

Personal Agent is designed as a stateful personal-agent runtime. LangGraph is the
control plane for state transitions; it is not the capability implementation and
the LLM is not the owner of irreversible actions.

## Bootstrap and composition root

Bootstrap runs before graph invocation and is outside the five-layer business
flow. It loads and validates typed application configuration, resolves the
repository/project paths, creates the currently available dependency objects,
constructs `RuntimeContext`, and compiles the LangGraph into an `Application`
container. It does not execute a task, parse CLI input, register placeholder
capabilities, read credential values, or connect an LLM.

The default configuration is located from the source package's repository root,
not from `os.getcwd()`. An explicit `config_path` takes precedence. Relative
paths in YAML, including a future file credential reference, are resolved from
the project root associated with the configuration file. Bootstrap only stores
credential references, so configured does not mean connected.

The development environment (Conda `pa` and installed packages) is separate from
application configuration (YAML values and references), which is separate from
runtime dependencies (`RuntimeContext` objects such as the empty capability
registry and compiled graph).

## Entry boundary

Entry is the boundary from the external world into an already-bootstrapped
runtime. CLI, web-shaped, and mobile-shaped user input is normalized into
`UserMessageInput`, then the Entry layer creates one `HumanMessage` and invokes
the graph. Entry does not create `SystemMessage`, `AIMessage`, or `ToolMessage`,
and it does not load configuration or construct dependencies.

Structured background events use the separate `BackgroundEventInput` contract.
They are not rewritten as user speech or `HumanMessage`; their Task/State
integration remains a later design step. A response to a paused graph is also a
different channel: future `resume_thread` handling will use LangGraph
`Command(resume=...)`, not a new user message. No interrupt/resume implementation
is connected yet.

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

The current formal State contract is `AgentState.messages`: the message history
shared by one graph execution/thread. Entry injects a `HumanMessage`; future
Agent/LLM and tool boundaries may return `AIMessage` and `ToolMessage` updates.
Nodes return partial updates such as `{"messages": [new_message]}`. LangGraph's
`add_messages` reducer merges those updates; it is a reducer, not a message
type. The current `task`, `artifacts`, `pending_action`, `status`, and `route`
fields remain scaffold/future fields. In particular, `route` is retained for
the current safe graph and does not yet represent a final routing contract.

State is execution-specific mutable data. RuntimeContext holds process
dependencies such as the model slot, capability registry, paths, logger, and
persistence slots. Neither layer owns the other's data: credentials, raw
configuration, workspace paths, and clients do not belong in State, while
messages and current actions do not belong in RuntimeContext.

## Agent and LLM boundary

The Agent node reads `AgentState.messages`, temporarily prepends the minimal
system prompt, and invokes the model from `RuntimeContext`. It returns an
`AIMessage` as a partial State update. The system prompt is model-call context,
not persisted State. Bootstrap constructs the configured DeepSeek model through
the LLM factory; the Agent does not read credentials or construct clients. Tool
binding is intentionally not active yet, and the current finalize route remains
a scaffold behavior.

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
