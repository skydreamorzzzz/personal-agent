# Bootstrap and Configuration

## Why split bootstrap from main

`main.py` should remain a thin process entry point. Composition belongs in one
place so configuration loading, dependency construction, and graph compilation
can be tested without introducing an Entry interaction layer.

## Composition root

`bootstrap_application()` is the composition root for v0.1. It creates typed
configuration, an empty CapabilityRegistry, RuntimeContext path wiring, and the
compiled LangGraph, then returns an Application container. It does not invoke the
graph or construct an LLM client.

## Configuration resolution

An explicit `config_path` wins. Otherwise the loader locates the repository root
from the package source location and uses `config/settings.yaml`; it does not
assume the current shell directory is the repository root. Relative YAML paths
are resolved from the configuration's project root.

## Credential handling

The typed configuration stores only the credential source and a reference (an
environment variable name or resolved file path). Bootstrap does not read a key,
read a secret file, or claim that an LLM is connected.

## Current reality

The real dependencies composed today are typed configuration, an empty capability
registry, RuntimeContext path wiring, and a compiled side-effect-free graph.
Model, checkpoint, memory, logger, Entry, and all capabilities remain
placeholders.

## Open questions

- Should missing environment credentials fail at composition time or only when a
  future LLM adapter is constructed?
- Which runtime directory creation policy should be adopted?
- Which RuntimeContext fields should become required once the first capability is
  implemented?
