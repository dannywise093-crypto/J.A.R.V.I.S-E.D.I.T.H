from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    x: float
    y: float
    width: float
    height: float


class VisionService:
    """Provider-neutral boundary for OpenCV/YOLO/MediaPipe integrations.

    Heavy CV dependencies stay outside the core API until a camera pipeline is enabled.
    """

    def status(self) -> dict[str, object]:
        return {"name": "E.D.I.T.H.", "ready": False, "provider": None}
