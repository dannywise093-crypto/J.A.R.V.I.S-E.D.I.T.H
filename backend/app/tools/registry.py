from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.core.policy import evaluate_tool


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def describe(self) -> list[dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

    async def execute(self, name: str, args: dict[str, Any], confirmed: bool = False) -> Any:
        decision = evaluate_tool(name, confirmed)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        if decision.requires_confirmation:
            return {"status": "confirmation_required", "reason": decision.reason, "tool": name}
        tool = self._tools.get(name)
        if not tool:
            raise KeyError(f"Unknown tool: {name}")
        return await tool.handler(**args)
