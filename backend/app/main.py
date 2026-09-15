from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.core.config import settings
from app.llm.provider import LLMProvider
from app.memory.store import MemoryStore
from app.tools.home_assistant import HomeAssistantClient
from app.tools.registry import Tool, ToolRegistry
from app.tools.system import system_status
from app.vision.service import VisionService

app = FastAPI(title="J.A.R.V.I.S.-E.D.I.T.H.", version="0.1.0")

memory = MemoryStore(settings.database_url)
llm = LLMProvider(settings.llm_base_url, settings.llm_model, settings.llm_api_key)
vision = VisionService()
tools = ToolRegistry()
tools.register(Tool("system_status", "Return basic assistant runtime status.", system_status))

if settings.home_assistant_url and settings.home_assistant_token:
    ha = HomeAssistantClient(settings.home_assistant_url, settings.home_assistant_token)

    async def ha_service(domain: str, service: str, service_data: dict | None = None):
        return await ha.service(domain, service, service_data)

    tools.register(Tool("home_assistant_service", "Call an explicitly authorized Home Assistant service.", ha_service))


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    confirmed_tool: str | None = None


class ToolRequest(BaseModel):
    name: str
    args: dict = Field(default_factory=dict)
    confirmed: bool = False


@app.get("/health")
async def health():
    return {"status": "ok", "service": "J.A.R.V.I.S.-E.D.I.T.H.", "vision": vision.status()}


@app.get("/tools")
async def list_tools():
    return {"tools": tools.describe()}


@app.post("/chat")
async def chat(request: ChatRequest):
    memory.add("user", request.message)
    messages = [
        {
            "role": "system",
            "content": (
                "You are J.A.R.V.I.S., a permission-first personal AI assistant. "
                "Never claim an external action happened unless a tool confirms it. "
                "Ask for confirmation before sensitive device actions."
            ),
        },
        *memory.recent(12),
    ]
    try:
        answer = await llm.chat(messages)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider unavailable: {exc}") from exc
    memory.add("assistant", answer)
    return {"assistant": answer, "model": settings.llm_model}


@app.post("/tools/execute")
async def execute_tool(request: ToolRequest):
    try:
        result = await tools.execute(request.name, request.args, request.confirmed)
        return {"tool": request.name, "result": result}
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
