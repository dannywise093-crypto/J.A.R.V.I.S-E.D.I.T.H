import sqlite3
from pathlib import Path


class MemoryStore:
    def __init__(self, database_url: str):
        path = database_url.removeprefix("sqlite:///")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, role TEXT NOT NULL, content TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
            )

    def add(self, role: str, content: str) -> None:
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO messages(role, content) VALUES (?, ?)", (role, content))

    def recent(self, limit: int = 12) -> list[dict[str, str]]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute(
                "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [{"role": role, "content": content} for role, content in reversed(rows)]
