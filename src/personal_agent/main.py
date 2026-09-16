"""Thin process entry point for application composition."""

from pathlib import Path

from personal_agent.application import Application
from personal_agent.bootstrap import bootstrap_application


def create_application(config_path: str | Path | None = None) -> Application:
    """Compose the application; Entry/UI is not implemented yet."""

    return bootstrap_application(config_path=config_path)


def main() -> Application:
    application = create_application()
    print("Entry layer is not implemented yet.")
    return application


if __name__ == "__main__":
    main()
