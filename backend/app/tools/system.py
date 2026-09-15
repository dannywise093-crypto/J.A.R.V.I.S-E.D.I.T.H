import platform
import time

START_TIME = time.time()


async def system_status() -> dict[str, str | float]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }
