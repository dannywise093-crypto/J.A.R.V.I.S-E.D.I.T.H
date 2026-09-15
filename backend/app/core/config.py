from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = ""

    database_url: str = "sqlite:///./jarvis.db"

    home_assistant_url: str = ""
    home_assistant_token: str = ""
    mqtt_host: str = ""
    mqtt_port: int = 1883
    mqtt_username: str = ""
    mqtt_password: str = ""

    require_confirmation_for_device_control: bool = True
    allowed_tool_names: str = "home_assistant_service,mqtt_publish,system_status"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_tools(self) -> set[str]:
        return {x.strip() for x in self.allowed_tool_names.split(",") if x.strip()}


settings = Settings()
