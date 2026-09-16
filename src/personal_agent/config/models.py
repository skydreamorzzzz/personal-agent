from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CredentialConfig:
    source: str
    env_name: str | None = None
    path: Path | None = None


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    credential: CredentialConfig
    endpoint: str | None = None


@dataclass(frozen=True)
class PathConfig:
    project_root: Path
    workspace: Path
    runtime_data: Path
    log: Path


@dataclass(frozen=True)
class AppConfig:
    llm: LLMConfig
    paths: PathConfig
