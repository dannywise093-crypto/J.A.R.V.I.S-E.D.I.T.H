# J.A.R.V.I.S.-E.D.I.T.H.

A modular, permission-first personal AI assistant platform combining conversational intelligence (J.A.R.V.I.S.) with visual awareness and telemetry (E.D.I.T.H.).

## Architecture

```text
Client / Voice / HUD
        |
        v
+----------------------+     +----------------------+
| J.A.R.V.I.S. Core   |<--->| E.D.I.T.H. Vision    |
| LLM + memory + plan |     | CV + telemetry       |
+----------+-----------+     +----------+-----------+
           |                            |
           +------------+---------------+
                        v
              +---------------------+
              | Tool / Policy Bus   |
              | auth + allowlists   |
              +----------+----------+
                         |
       +-----------------+------------------+
       |                 |                  |
       v                 v                  v
  Home Assistant       MQTT          Authorized APIs

Local-first operation is preferred. Cloud providers are optional adapters.
```

## Current foundation

- Python/FastAPI service with health and chat endpoints.
- Provider abstraction for Ollama and OpenAI-compatible APIs.
- Conversation memory using SQLite, with an optional vector-memory adapter boundary.
- Permissioned tool registry: tools are explicitly registered and can require confirmation.
- Home Assistant and MQTT adapters designed around user-supplied credentials.
- Vision service boundary for OpenCV/YOLO integration without forcing heavy dependencies on the core server.
- Configuration through environment variables; secrets are never committed.
- Docker Compose for the core API and optional services.
- Automated tests for policy and core routing.

## Safety and security model

J.A.R.V.I.S.-E.D.I.T.H. is designed to control only systems that the user has explicitly authorized. There is no covert device access, credential harvesting, persistence mechanism, or arbitrary remote command execution.

Sensitive actions should require explicit confirmation. Device integrations use scoped credentials, audit logs, and allowlists. Remote access should be placed behind a VPN or zero-trust gateway rather than exposing the assistant directly to the public internet.

## Quick start

1. Copy `.env.example` to `.env` and configure an LLM provider.
2. Install Python 3.11+ dependencies from `backend/requirements.txt`.
3. Run `uvicorn app.main:app --reload --app-dir backend`.
4. Open `/docs` for the API.

For local LLM use, Ollama can provide an OpenAI-compatible endpoint. Cloud providers can be added through provider adapters without changing the tool bus.

## Roadmap

### Phase 1 — Core
- [x] API skeleton
- [x] provider abstraction
- [x] policy/confirmation boundary
- [x] local conversation memory
- [x] health/telemetry endpoint

### Phase 2 — Voice
- [ ] wake-word adapter
- [ ] Faster-Whisper streaming adapter
- [ ] Piper/XTTS adapter
- [ ] mobile voice client

### Phase 3 — E.D.I.T.H. vision
- [ ] OpenCV camera adapter
- [ ] YOLO object detection adapter
- [ ] MediaPipe tracking adapter
- [ ] HUD/AR telemetry protocol

### Phase 4 — Home/device control
- [ ] Home Assistant device discovery through authorized API
- [ ] MQTT device adapter
- [ ] routines and schedules
- [ ] confirmation policies for sensitive actions

### Phase 5 — Remote architecture
- [ ] authenticated mobile gateway
- [ ] WebSocket event stream
- [ ] VPN/zero-trust deployment guide
- [ ] multi-device identity and revocation

## Project layout

```text
backend/
  app/
    core/       settings, policy, models
    llm/        model-provider adapters
    memory/     conversation persistence
    tools/      permissioned execution tools
    vision/     E.D.I.T.H. vision boundary
    main.py     FastAPI entrypoint
  tests/
config/
docs/
```

## License

Choose and add a license before distributing the project.