import contextlib
import importlib.util
import io
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "authrequest_gc.py"
SPEC = importlib.util.spec_from_file_location("authrequest_gc", SCRIPT)
GC = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GC
SPEC.loader.exec_module(GC)


class FakeApi:
    def __init__(self, pages=(), delete_statuses=()):
        self.pages = iter(pages)
        self.delete_statuses = iter(delete_statuses)
        self.calls = []

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if method == "GET":
            return 200, json.dumps(next(self.pages)).encode()
        return next(self.delete_statuses), b""


def authrequest(name, expiry, namespace="networking"):
    return {
        "metadata": {"name": name, "namespace": namespace},
        "expiry": expiry,
    }


class AuthRequestGcTests(unittest.TestCase):
    def test_paginates_and_selects_only_expired_requests_in_namespace(self):
        now = datetime(2026, 10, 27, 20, 0, tzinfo=timezone.utc)
        pages = [
            {
                "items": [
                    authrequest("expired-one", "2026-10-27T19:00:00Z"),
                    authrequest("still-valid", "2026-10-27T21:00:00Z"),
                ],
                "metadata": {"continue": "next/page"},
            },
            {
                "items": [
                    authrequest("expired-two", "2026-10-27T18:00:00Z"),
                    authrequest("other-namespace", "2026-10-27T18:00:00Z", "other"),
                ],
                "metadata": {"continue": ""},
            },
        ]
        api = FakeApi(pages=pages)

        with contextlib.redirect_stdout(io.StringIO()):
            scanned, expired = GC.collect_expired(api, now)

        self.assertEqual(scanned, 4)
        self.assertEqual([name for _, name in expired], ["expired-one", "expired-two"])
        self.assertEqual(len([call for call in api.calls if call[0] == "GET"]), 2)

    def test_deletes_expired_only_and_tolerates_already_removed_records(self):
        expired = [
            (datetime(2026, 10, 27, 18, 0, tzinfo=timezone.utc), "old-one"),
            (datetime(2026, 10, 27, 19, 0, tzinfo=timezone.utc), "old-two"),
        ]
        api = FakeApi(delete_statuses=[200, 404])

        with patch.object(GC, "DELETE_QPS", 1_000_000), patch.object(GC.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            deleted, already_gone, deferred = GC.delete_expired(api, expired)

        self.assertEqual((deleted, already_gone, deferred), (1, 1, 0))
        self.assertEqual([call[0] for call in api.calls], ["DELETE", "DELETE"])
        self.assertIn("/networking/authrequests/old-one", api.calls[0][1])
        self.assertIn("/networking/authrequests/old-two", api.calls[1][1])


if __name__ == "__main__":
    unittest.main()
