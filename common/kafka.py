"""Kafka stubs for future expansion."""
from __future__ import annotations

from typing import Any


class DummyProducer:
    def send(self, topic: str, value: Any) -> None:  # pragma: no cover - stub
        return None


class DummyConsumer:
    def poll(self, timeout: float = 1.0) -> list[Any]:  # pragma: no cover - stub
        return []


def create_producer() -> DummyProducer:
    return DummyProducer()


def create_consumer() -> DummyConsumer:
    return DummyConsumer()
