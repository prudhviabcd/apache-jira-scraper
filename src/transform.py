from typing import Dict, Any, List
from  .utils import strip_html

def transform_issue(issue: Dict[str, Any], comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    f = issue.get("fields", {})
    meta = {
        "title": f.get("summary"),
        "status": (f.get("status") or {}).get("name"),
        "priority": (f.get("priority") or {}).get("name"),
        "assignee": ((f.get("assignee") or {}) or {}).get("displayName"),
        "labels": f.get("labels") or [],
        "reporter": (f.get("reporter") or {}).get("displayName"),
        "created": f.get("created"),
        "updated": f.get("updated"),
        "issuetype": (f.get("issuetype") or {}).get("name"),
        "project": ((f.get("project") or {}) or {}).get("key") or None,
        "key": issue.get("key"),
    }

    record = {
        "project": meta["project"],
        "issue_key": meta["key"],
        "metadata": meta,
        "description": strip_html(f.get("description")),
        "comments": [strip_html(c.get("body")) for c in (comments or [])],
        # Example derived field for downstream tasks; feel free to extend
        "derived": {
            "classification_target": meta["status"],
        },
    }
    return record
