import os
import json
from typing import List, Dict, Any
from tqdm import tqdm

from src .jira_client import JiraClient
from src .transform import transform_issue
from src .utils import Checkpointer

BASE_URL = "https://issues.apache.org/jira"

def export_jsonl(path: str, items: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def scrape_project(project_key: str, output_dir: str, page_size: int, retry_conf: Dict[str, Any]):
    client = JiraClient(
        BASE_URL,
        max_retries=retry_conf.get("max_retries", 5),
        base_sleep=retry_conf.get("base_sleep_seconds", 2),
        max_sleep=retry_conf.get("max_sleep_seconds", 60),
    )

    checkpoint = Checkpointer(os.path.join("checkpoints", f"{project_key}.json"))
    state = checkpoint.load()
    last_updated_iso = state.get("last_updated_iso")
    seen_keys = set(state.get("seen_keys", []))

    # Build JQL that supports resume by "updated" field and stable ordering
    jql = f'project={project_key} ORDER BY updated ASC'
    if last_updated_iso:
        jql = f'project={project_key} AND updated >= "{last_updated_iso}" ORDER BY updated ASC'

    start_at = 0
    total = None
    out_path = os.path.join(output_dir, f"{project_key}.jsonl")

    pbar = tqdm(desc=f"{project_key}", unit="issue")
    while True:
        page = client.search_issues(jql=jql, start_at=start_at, max_results=page_size)
        total = page.get("total", 0) if total is None else total
        issues = page.get("issues", [])

        if not issues:
            break

        batch_records = []
        for issue in issues:
            key = issue.get("key")
            # Deduplicate if resuming on same timestamp window
            if key in seen_keys:
                continue

            # Collect all comments (paginated)
            comments_all = []
            cm_start = 0
            while True:
                cm = client.get_issue_comments(key, start_at=cm_start, max_results=100)
                values = cm.get("comments", [])
                if not values:
                    break
                comments_all.extend(values)
                cm_start += len(values)
                if cm_start >= (cm.get("total") or 0):
                    break

            record = transform_issue(issue, comments_all)
            batch_records.append(record)

            # Update checkpoint live for fault tolerance
            seen_keys.add(key)
            checkpoint.add_seen(key)

            # Track last updated for resume
            fields = issue.get("fields", {})
            last_updated_iso = fields.get("updated") or last_updated_iso
            if last_updated_iso:
                checkpoint.update_last_updated(last_updated_iso)

            pbar.update(1)

        export_jsonl(out_path, batch_records)
        start_at += len(issues)

        # If the server returns fewer than page_size, we're at the end
        if len(issues) < page_size:
            break

    pbar.close()
