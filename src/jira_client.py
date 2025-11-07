import time
from typing import Dict, Any, Optional, List
import requests

class JiraClient:
    def __init__(self, base_url: str, max_retries: int = 5, base_sleep: int = 2, max_sleep: int = 60):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.max_retries = max_retries
        self.base_sleep = base_sleep
        self.max_sleep = max_sleep

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        attempt = 0
        sleep_s = self.base_sleep
        while True:
            attempt += 1
            try:
                resp = self.session.request(method, url, timeout=60, **kwargs)
            except requests.RequestException as e:
                if attempt >= self.max_retries:
                    raise
                time.sleep(min(sleep_s, self.max_sleep))
                sleep_s *= 2
                continue

            # Handle rate limiting and server errors
            if resp.status_code in (429, 502, 503, 504, 500):
                if attempt >= self.max_retries:
                    resp.raise_for_status()
                # Respect Retry-After if present
                retry_after = resp.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait = int(retry_after)
                    except ValueError:
                        wait = sleep_s
                else:
                    wait = sleep_s
                time.sleep(min(wait, self.max_sleep))
                sleep_s = min(sleep_s * 2, self.max_sleep)
                continue

            # For other 4xx, raise immediately
            if 400 <= resp.status_code < 500:
                resp.raise_for_status()

            return resp

    def search_issues(self, jql: str, start_at: int = 0, max_results: int = 100, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
        }
        # Ask Jira to include only fields we need; avoids big payloads
        if fields:
            params["fields"] = ",".join(fields)
        else:
            params["fields"] = "summary,status,priority,assignee,labels,reporter,description,issuetype,project,created,updated"
        # API v2
        resp = self._request("GET", "/rest/api/2/search", params=params)
        return resp.json()

    def get_issue_comments(self, issue_key: str, start_at: int = 0, max_results: int = 100) -> Dict[str, Any]:
        params = {"startAt": start_at, "maxResults": max_results}
        resp = self._request("GET", f"/rest/api/2/issue/{issue_key}/comment", params=params)
        return resp.json()
