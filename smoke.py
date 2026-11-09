"""Run a small real inference test; credentials stay in environment variables."""
import json
import os
import urllib.error
import urllib.request

base = os.environ["GATEWAY_URL"].rstrip("/")
master = os.environ["LITELLM_MASTER_KEY"]


def request(path, payload=None, key=None):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            request.last_headers = dict(response.headers)
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, {}


status, readiness = request("/health/readiness")
assert status == 200, ("readiness", status)
assert readiness.get("db") == "connected", "Database not connected"
print("PASS readiness: PostgreSQL connected")
status, _ = request("/v1/models")
assert status in (401, 403), ("unauthenticated request", status)
print("PASS unauthenticated model access rejected")
status, created = request("/key/generate", {"models": ["chat", "backup"], "duration": "1h"}, master)
assert status == 200 and created.get("key"), ("virtual key generation", status)
app_key = created["key"]
print("PASS restricted application key created")
try:
    if os.environ.get("EXPECT_FALLBACK") == "1":
        status, info = request("/model/info", key=master)
        assert status == 200, ("model info", status)
        backup_id = next(str(m["model_info"]["id"]) for m in info["data"] if m["model_name"] == "backup")
    status, response = request("/v1/chat/completions", {
        "model": os.environ.get("TEST_MODEL", "chat"),
        "messages": [{"role": "user", "content": "Reply with exactly: gateway works"}],
        "max_tokens": 16,
    }, app_key)
    assert status == 200 and response.get("choices"), ("completion", status)
    if os.environ.get("EXPECT_FALLBACK") == "1":
        headers = {k.lower(): v for k, v in request.last_headers.items()}
        assert headers.get("x-litellm-model-id") == backup_id, "Expected backup model ID in response headers"
        print("PASS configured backup model served the request")
    print("PASS inference:", response["model"], json.dumps(response["choices"][0]["message"]["content"]))
    print("Usage:", json.dumps(response.get("usage", {})))
finally:
    status, _ = request("/key/delete", {"keys": [app_key]}, master)
    assert status == 200, ("temporary key cleanup", status)
    print("PASS temporary application key revoked")
