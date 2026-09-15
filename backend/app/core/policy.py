from dataclasses import dataclass

from .config import settings


@dataclass(frozen=True)
class ToolDecision:
    allowed: bool
    requires_confirmation: bool
    reason: str


def evaluate_tool(name: str, requested_confirmation: bool = False) -> ToolDecision:
    if name not in settings.allowed_tools:
        return ToolDecision(False, False, "Tool is not on the configured allowlist.")

    device_tool = name in {"home_assistant_service", "mqtt_publish"}
    if device_tool and settings.require_confirmation_for_device_control and not requested_confirmation:
        return ToolDecision(True, True, "Device control requires explicit confirmation.")

    return ToolDecision(True, False, "Tool is permitted by policy.")
