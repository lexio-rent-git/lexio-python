"""Suit le flux d'événements Lexio Rent et garde le curseur dans un fichier.

    export LEXIO_API_KEY="lck_..."
    python examples/sync_events.py            # à lancer en cron toutes les minutes
"""
from __future__ import annotations

import json
import pathlib

from lexio_rent import Lexio

STATE = pathlib.Path(".lexio_cursor")


def main() -> None:
    cursor = STATE.read_text().strip() if STATE.exists() else None
    with Lexio() as lexio:
        while True:
            page = lexio.events.list(cursor=cursor, limit=100) if cursor else lexio.events.list(start="EARLIEST", limit=100)
            for event in page["data"]:
                print(json.dumps(event, ensure_ascii=False))
            new_cursor = page.get("nextCursor")
            if new_cursor:
                cursor = new_cursor
                STATE.write_text(cursor)
            if not page["data"]:
                break


if __name__ == "__main__":
    main()
