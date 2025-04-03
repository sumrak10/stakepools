import uvicorn

from src.config.server import server_settings
from src.infrastructure.fastapi.app import create_app
from src.infrastructure.logger.logger import LoggerConfig


def main() -> None:
    LoggerConfig.setup_logger()

    app = create_app()
    uvicorn.run(
        app,
        host=server_settings.HOST,
        port=server_settings.PORT
    )
