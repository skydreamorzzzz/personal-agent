from pathlib import Path

from personal_agent.application import Application
from personal_agent.capabilities.registry import CapabilityRegistry
from personal_agent.config import ConfigurationError, load_config
from personal_agent.runtime.builder import build_graph
from personal_agent.runtime.context import RuntimeContext


class BootstrapError(RuntimeError):
    """Raised when application composition cannot be completed."""


def bootstrap_application(config_path: str | Path | None = None) -> Application:
    """Load configuration and compose the safe v0.1 runtime.

    This function keeps credential references only. It does not read credential
    values, construct an LLM client, create directories, or invoke the graph.
    """

    try:
        config = load_config(config_path)
        registry = CapabilityRegistry()
        context = RuntimeContext(
            model=None,
            workspace_path=config.paths.workspace,
            runtime_data_path=config.paths.runtime_data,
            log_path=config.paths.log,
            capability_registry=registry,
        )
        graph = build_graph()
        return Application(config=config, graph=graph, context=context)
    except ConfigurationError:
        raise
    except Exception as exc:
        raise BootstrapError("Unable to compose application runtime") from exc
