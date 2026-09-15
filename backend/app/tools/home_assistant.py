import httpx


class HomeAssistantClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def service(self, domain: str, service: str, service_data: dict | None = None) -> dict:
        if not self.base_url or not self.token:
            raise RuntimeError("Home Assistant is not configured.")
        if not domain.replace("_", "").isalnum() or not service.replace("_", "").isalnum():
            raise ValueError("Invalid Home Assistant service identifier.")
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                f"{self.base_url}/api/services/{domain}/{service}",
                json=service_data or {},
                headers=headers,
            )
            response.raise_for_status()
            return {"ok": True, "status_code": response.status_code, "result": response.json()}
