#!/usr/bin/env python3
"""Paginate Dex AuthRequests and delete only entries past their stored expiry."""

import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

NAMESPACE = os.environ.get("DEX_NAMESPACE", "networking")
RESOURCE_PATH = f"/apis/dex.coreos.com/v1/namespaces/{NAMESPACE}/authrequests"
SERVICE_ACCOUNT_DIR = Path("/var/run/secrets/kubernetes.io/serviceaccount")
PAGE_SIZE = int(os.environ.get("PAGE_SIZE", "500"))
MAX_DELETES = int(os.environ.get("MAX_DELETES", "100000"))
DELETE_QPS = float(os.environ.get("DELETE_QPS", "20"))
HTTP_TIMEOUT = float(os.environ.get("HTTP_TIMEOUT_SECONDS", "30"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "5"))


def emit(event, **fields):
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "component": "dex-authrequest-gc",
        "event": event,
        **fields,
    }
    print(json.dumps(record, separators=(",", ":")), flush=True)


def parse_time(value):
    if not value:
        raise ValueError("AuthRequest is missing expiry")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class KubernetesApi:
    def __init__(self):
        host = os.environ["KUBERNETES_SERVICE_HOST"]
        port = os.environ.get("KUBERNETES_SERVICE_PORT_HTTPS", "443")
        self.base_url = f"https://{host}:{port}"
        self.token_path = SERVICE_ACCOUNT_DIR / "token"
        self.token = self.token_path.read_text().strip()
        self.context = ssl.create_default_context(cafile=str(SERVICE_ACCOUNT_DIR / "ca.crt"))

    def request(self, method, path, payload=None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        refreshed_token = False
        for attempt in range(MAX_RETRIES + 1):
            headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
            if body is not None:
                headers["Content-Type"] = "application/json"
            request = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(request, context=self.context, timeout=HTTP_TIMEOUT) as response:
                    return response.status, response.read()
            except urllib.error.HTTPError as error:
                response_body = error.read()
                if error.code == 404 and method == "DELETE":
                    return 404, response_body
                if error.code == 401 and not refreshed_token:
                    self.token = self.token_path.read_text().strip()
                    refreshed_token = True
                    continue
                if error.code != 429 and not 500 <= error.code < 600:
                    return error.code, response_body
                retry_after = error.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else min(2**attempt, 30)
                emit("api_retry", method=method, status=error.code, attempt=attempt + 1, delay_seconds=delay)
                time.sleep(delay)
            except (urllib.error.URLError, TimeoutError) as error:
                if attempt >= MAX_RETRIES:
                    raise RuntimeError(f"Kubernetes API {method} request failed after retries: {type(error).__name__}") from error
                delay = min(2**attempt, 30)
                emit("api_retry", method=method, error=type(error).__name__, attempt=attempt + 1, delay_seconds=delay)
                time.sleep(delay)
        raise RuntimeError(f"Kubernetes API {method} request exhausted retries")


def collect_expired(api, now):
    continuation = ""
    page_number = 0
    scanned = 0
    expired = []

    while True:
        query = {"limit": str(PAGE_SIZE)}
        if continuation:
            query["continue"] = continuation
        path = RESOURCE_PATH + "?" + urllib.parse.urlencode(query)
        status, body = api.request("GET", path)
        if status != 200:
            raise RuntimeError(f"AuthRequest list failed with HTTP {status}")

        page = json.loads(body)
        items = page.get("items", [])
        page_expired = []
        for item in items:
            metadata = item.get("metadata", {})
            if metadata.get("namespace") != NAMESPACE:
                continue
            expiry = parse_time(item.get("expiry"))
            if expiry < now:
                page_expired.append((expiry, metadata["name"]))

        page_number += 1
        scanned += len(items)
        expired.extend(page_expired)
        continuation = page.get("metadata", {}).get("continue", "")
        emit(
            "page_scanned",
            page=page_number,
            page_items=len(items),
            page_expired=len(page_expired),
            scanned_total=scanned,
            expired_total=len(expired),
            has_more=bool(continuation),
        )
        if not continuation:
            break

    return scanned, expired


def delete_expired(api, expired):
    expired.sort(key=lambda item: (item[0], item[1]))
    selected = expired[:MAX_DELETES]
    deferred = len(expired) - len(selected)
    emit("delete_started", expired_found=len(expired), selected=len(selected), deferred=deferred, qps=DELETE_QPS)

    interval = 1.0 / DELETE_QPS
    next_request = time.monotonic()
    started = next_request
    deleted = 0
    already_gone = 0
    delete_options = {"apiVersion": "v1", "kind": "DeleteOptions", "propagationPolicy": "Background"}

    for index, (_, name) in enumerate(selected, start=1):
        delay = next_request - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        encoded_name = urllib.parse.quote(name, safe="")
        path = f"{RESOURCE_PATH}/{encoded_name}"
        status, _ = api.request("DELETE", path, delete_options)
        next_request = max(next_request + interval, time.monotonic())

        if status in (200, 202, 204):
            deleted += 1
        elif status == 404:
            already_gone += 1
        else:
            emit("delete_failed", status=status, attempted=index - 1, remaining=len(selected) - index + 1)
            raise RuntimeError(f"AuthRequest deletion failed with HTTP {status}")

        if index % 1000 == 0 or index == len(selected):
            elapsed = max(time.monotonic() - started, 0.001)
            emit(
                "delete_progress",
                attempted=index,
                target=len(selected),
                deleted=deleted,
                already_gone=already_gone,
                elapsed_seconds=round(elapsed, 1),
                average_qps=round(index / elapsed, 2),
            )

    return deleted, already_gone, deferred


def main():
    if PAGE_SIZE < 1 or MAX_DELETES < 1 or DELETE_QPS <= 0:
        raise ValueError("PAGE_SIZE, MAX_DELETES, and DELETE_QPS must be positive")
    now = datetime.now(timezone.utc)
    started = time.monotonic()
    emit("run_started", namespace=NAMESPACE, snapshot_time=now.isoformat(), page_size=PAGE_SIZE, max_deletes=MAX_DELETES)

    api = KubernetesApi()
    scanned, expired = collect_expired(api, now)
    emit("inventory_complete", scanned=scanned, expired=len(expired), unexpired=scanned - len(expired))
    deleted, already_gone, deferred = delete_expired(api, expired)
    emit(
        "run_finished",
        scanned=scanned,
        expired_found=len(expired),
        deleted=deleted,
        already_gone=already_gone,
        deferred=deferred,
        elapsed_seconds=round(time.monotonic() - started, 1),
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        emit("run_failed", error=type(error).__name__, message=str(error))
        sys.exit(1)
