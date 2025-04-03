from __future__ import annotations


class HealthCheckError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseHealthCheckError(HealthCheckError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Database healthcheck failed")

