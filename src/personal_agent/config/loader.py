from pathlib import Path
from typing import Any

import yaml

from personal_agent.config.models import AppConfig, CredentialConfig, LLMConfig, PathConfig


class ConfigurationError(ValueError):
    """Raised when application configuration is missing or malformed."""


_DEFAULT_CONFIG_RELATIVE_PATH = Path("config") / "settings.yaml"
_DEFAULT_PATHS = {
    "workspace": Path("workspace"),
    "runtime_data": Path("data") / "runtime",
    "log": Path("log") / "runtime",
}


def _repository_root() -> Path:
    """Find the repository root without consulting the current cwd."""

    for parent in Path(__file__).resolve().parents:
        if (parent / _DEFAULT_CONFIG_RELATIVE_PATH).is_file():
            return parent
    raise ConfigurationError(
        "Default config/settings.yaml could not be located from the package"
    )


def _resolve_config_path(config_path: str | Path | None) -> tuple[Path, Path]:
    if config_path is None:
        project_root = _repository_root()
        return project_root / _DEFAULT_CONFIG_RELATIVE_PATH, project_root

    path = Path(config_path).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    project_root = path.parent.parent if path.parent.name == "config" else path.parent
    return path, project_root


def _mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"Configuration section '{name}' must be a mapping")
    return value


def _required_string(section: dict[str, Any], key: str, name: str) -> str:
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"Missing or invalid configuration field: {name}.{key}")
    return value.strip()


def _resolve_path(value: Any, project_root: Path, name: str, default: Path) -> Path:
    raw = default if value is None else value
    if isinstance(raw, Path):
        path = raw
    elif isinstance(raw, str) and raw.strip():
        path = Path(raw).expanduser()
    else:
        raise ConfigurationError(f"Invalid path configuration: {name}")
    if isinstance(raw, Path):
        path = raw.expanduser()
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigurationError(f"Configuration file does not exist: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"Invalid YAML in configuration file: {path}") from exc
    except OSError as exc:
        raise ConfigurationError(f"Unable to read configuration file: {path}") from exc
    return _mapping(data, "root")


def _load_credential(section: dict[str, Any], project_root: Path) -> CredentialConfig:
    source = _required_string(section, "source", "llm.credential")
    if source not in {"env", "file"}:
        raise ConfigurationError("Invalid credential source; expected 'env' or 'file'")

    if source == "env":
        env_name = _required_string(section, "env_name", "llm.credential")
        return CredentialConfig(source=source, env_name=env_name)

    raw_path = section.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ConfigurationError("Missing or invalid configuration field: llm.credential.path")
    credential_path = Path(raw_path).expanduser()
    if not credential_path.is_absolute():
        credential_path = project_root / credential_path
    return CredentialConfig(source=source, path=credential_path.resolve())


def load_config(config_path: str | Path | None = None) -> AppConfig:
    """Load typed configuration without reading credential values."""

    path, project_root = _resolve_config_path(config_path)
    raw = _load_yaml(path)
    llm_section = _mapping(raw.get("llm"), "llm")
    provider = _required_string(llm_section, "provider", "llm")
    model = _required_string(llm_section, "model", "llm")
    credential_section = _mapping(llm_section.get("credential"), "llm.credential")
    credential = _load_credential(credential_section, project_root)

    endpoint = llm_section.get("endpoint")
    if endpoint is not None and (not isinstance(endpoint, str) or not endpoint.strip()):
        raise ConfigurationError("Invalid configuration field: llm.endpoint")

    paths_section = _mapping(raw.get("paths", {}), "paths")
    paths = PathConfig(
        project_root=project_root,
        workspace=_resolve_path(paths_section.get("workspace"), project_root, "paths.workspace", _DEFAULT_PATHS["workspace"]),
        runtime_data=_resolve_path(paths_section.get("runtime_data"), project_root, "paths.runtime_data", _DEFAULT_PATHS["runtime_data"]),
        log=_resolve_path(paths_section.get("log"), project_root, "paths.log", _DEFAULT_PATHS["log"]),
    )
    return AppConfig(
        llm=LLMConfig(
            provider=provider,
            model=model,
            credential=credential,
            endpoint=endpoint.strip() if isinstance(endpoint, str) else None,
        ),
        paths=paths,
    )
