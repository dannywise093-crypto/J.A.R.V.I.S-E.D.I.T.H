# J.A.R.V.I.S.-E.D.I.T.H. Architecture

## Runtime flow

1. Client sends text or, later, audio/image input.
2. J.A.R.V.I.S. creates context from recent memory.
3. LLM produces a response or proposes a tool operation.
4. Policy engine checks whether the tool is allowed and whether confirmation is required.
5. Tool adapter talks only to configured, authorized services.
6. Result is returned to the assistant and logged.

## J.A.R.V.I.S.

The intelligence layer is provider-neutral. The current implementation speaks the OpenAI-compatible Chat Completions protocol, which lets local Ollama deployments and compatible cloud gateways sit behind the same adapter.

## E.D.I.T.H.

Vision is deliberately isolated from the API core. Future adapters can provide OpenCV frames, YOLO detections, MediaPipe landmarks, or multimodal model results. The core should consume normalized detections and telemetry rather than depend on one CV vendor.

## Voice

Planned pipeline:

```text
microphone -> wake word -> STT -> J.A.R.V.I.S. -> TTS -> speaker/HUD
```

Faster-Whisper, Porcupine, Piper, or another compatible provider can be added as adapters. Audio processing should be opt-in and indicator-visible when a microphone is active.

## Device control

Home Assistant and MQTT integrations are treated as controlled execution surfaces. The assistant must never accept arbitrary shell commands as a general-purpose tool. Every device action is allowlisted, authenticated, auditable, and confirmation-gated where configured.

## Remote access

For remote access, deploy the API behind an authenticated VPN or zero-trust gateway. Do not expose the raw API to the public internet. Each device should have its own identity and revocation path in a production deployment.

## Data

SQLite is the initial local memory store. Qdrant/Chroma can be added behind a memory interface for semantic retrieval. Sensitive memory should have explicit retention and deletion controls before production use.
