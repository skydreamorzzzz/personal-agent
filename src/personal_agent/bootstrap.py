from pathlib import Path
from personal_agent.application import Application
from personal_agent.capabilities.registry import CapabilityRegistry
from personal_agent.config import ConfigurationError, load_config
from personal_agent.runtime.builder import build_graph
from personal_agent.runtime.context import RuntimeContext
from personal_agent.llm.client import (
    LLMConfigurationError,
    ModelFactory,
    build_chat_model,
)


class BootstrapError(RuntimeError):
    """Raised when application composition cannot be completed."""


def bootstrap_application(
    config_path: str | Path | None = None,
    model_factory: ModelFactory = build_chat_model,
) -> Application:
    """Load configuration and compose the model-backed v0.1 runtime.

    The factory resolves credentials only inside the LLM boundary. Bootstrap
    does not invoke the graph or create runtime directories.
    """

    try:
        config = load_config(config_path)
        registry = CapabilityRegistry()
        model = model_factory(config.llm)
        context = RuntimeContext(
            model=model,
            workspace_path=config.paths.workspace,
            runtime_data_path=config.paths.runtime_data,
            log_path=config.paths.log,
            capability_registry=registry,
        )
        graph = build_graph()
        return Application(config=config, graph=graph, context=context)
    except (ConfigurationError, LLMConfigurationError):
        raise
    except Exception as exc:
        raise BootstrapError("Unable to compose application runtime") from exc
