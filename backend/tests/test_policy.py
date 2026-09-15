from app.core.policy import evaluate_tool


def test_unknown_tool_denied():
    decision = evaluate_tool("unknown_tool")
    assert not decision.allowed


def test_device_tool_requires_confirmation():
    decision = evaluate_tool("home_assistant_service")
    assert decision.allowed
    assert decision.requires_confirmation


def test_confirmed_device_tool_allowed():
    decision = evaluate_tool("home_assistant_service", requested_confirmation=True)
    assert decision.allowed
    assert not decision.requires_confirmation
