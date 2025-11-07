import time
import json
import os
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup

def strip_html(html: Optional[str]) -> str:
    """Convert Jira's HTML/markup to plain text safely."""
    if not html:
        return ""
    # Jira often returns wiki/HTML-ish bodies; BeautifulSoup handles it fairly.
    try:
        soup = BeautifulSoup(html, "html.parser")
        # Keep line breaks for <br> and block elements
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = soup.get_text(separator="\n")
        # Normalize whitespace
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip() != "")
        return text
    except Exception:
        # Fallback to raw string if parsing fails
        return str(html)

class Checkpointer:
    """File-based checkpoint per project to support resume & idempotence."""
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        if not os.path.exists(self.path):
            self.save({"last_updated_iso": None, "seen_keys": []})

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"last_updated_iso": None, "seen_keys": []}

    def save(self, state: Dict[str, Any]):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        import shutil
        shutil.move(tmp,self.path)

    def update_last_updated(self, iso_str: Optional[str]):
        state = self.load()
        state["last_updated_iso"] = iso_str
        self.save(state)

    def add_seen(self, issue_key: str, keep_last: int = 5000):
        state = self.load()
        seen = state.get("seen_keys", [])
        seen.append(issue_key)
        # Avoid unbounded growth; keep most recent N
        state["seen_keys"] = seen[-keep_last:]
        self.save(state)
