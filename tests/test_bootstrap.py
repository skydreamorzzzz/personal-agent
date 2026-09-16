import pytest

from personal_agent.application import Application
from personal_agent.bootstrap import bootstrap_application
from personal_agent.config import ConfigurationError, load_config


def test_default_config_loads():
    config = load_config()

    assert config.llm.provider == "deepseek"
    assert config.paths.project_root.name == "personal-agent"
    assert config.llm.credential.env_name == "DEEPSEEK_API_KEY"


def test_explicit_config_path_loads(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "settings.yaml"
    config_path.write_text(
        "llm:\n"
        "  provider: test-provider\n"
        "  model: test-model\n"
        "  credential:\n"
        "    source: env\n"
        "    env_name: TEST_API_KEY\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.llm.model == "test-model"
    assert config.paths.project_root == tmp_path


def test_default_config_does_not_depend_on_cwd(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config.paths.project_root != tmp_path
    assert config.paths.workspace == config.paths.project_root / "workspace"


def test_invalid_yaml_has_clear_error(tmp_path):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text("llm: [broken", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Invalid YAML") as error:
        load_config(config_path)

    assert "DEEPSEEK_API_KEY" not in str(error.value)


def test_invalid_config_has_clear_error(tmp_path):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text(
        "llm:\n"
        "  provider: deepseek\n"
        "  model: deepseek-chat\n"
        "  credential:\n"
        "    source: unsupported\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError, match="credential source"):
        load_config(config_path)


def test_missing_required_field_has_clear_error(tmp_path):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text("llm:\n  provider: deepseek\n", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="llm.model"):
        load_config(config_path)


def test_file_credential_path_is_resolved_without_reading_file(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "settings.yaml"
    config_path.write_text(
        "llm:\n"
        "  provider: deepseek\n"
        "  model: deepseek-chat\n"
        "  credential:\n"
        "    source: file\n"
        "    path: secret/llm/API.txt\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.llm.credential.path == tmp_path / "secret/llm/API.txt"


def test_missing_env_credential_is_not_read_or_required(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)

    application = bootstrap_application()

    assert application.config.llm.credential.env_name == "DEEPSEEK_API_KEY"
    assert application.context.model is None


def test_bootstrap_returns_application_with_empty_registry():
    application = bootstrap_application()

    assert isinstance(application, Application)
    assert application.graph is not None
    assert application.context.capability_registry.schemas() == []
    assert application.context.workspace_path == application.config.paths.workspace


def test_bootstrap_does_not_create_runtime_directories(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "settings.yaml"
    config_path.write_text(
        "llm:\n"
        "  provider: deepseek\n"
        "  model: deepseek-chat\n"
        "  credential:\n"
        "    source: env\n"
        "    env_name: TEST_API_KEY\n"
        "paths:\n"
        "  workspace: workspace\n"
        "  runtime_data: runtime\n"
        "  log: logs\n",
        encoding="utf-8",
    )

    bootstrap_application(config_path)

    assert not (tmp_path / "workspace").exists()
    assert not (tmp_path / "runtime").exists()
    assert not (tmp_path / "logs").exists()
