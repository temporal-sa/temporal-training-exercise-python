"""
ABOUTME: mitmproxy addon that reads /root/proxy/state.json and blocks or passes
outbound requests based on which service groups are toggled off.

Ported from temporal-sa/ai-agents-webinar. The host map is scoped to what the
Temporal in Practice sandbox actually reaches: the Python package index, GitHub,
and a request-echo service used to prove the proxy is in the path.

State file format:
{
  "kill_all": false,
  "services": {
    "pypi":    true,
    "github":  true,
    "httpbin": true
  }
}
A value of true means the service is ALLOWED through.

To add a toggle:
  1. Add the key and its hostnames to SERVICE_HOSTS below.
  2. Add the key with `true` to state.json.
  3. Add the key and a display label to SERVICE_LABELS in controlpanel.py.
The control panel renders its toggles from SERVICE_LABELS, so no HTML changes
are needed.
"""
import json
from mitmproxy import http

STATE_FILE = "/root/proxy/state.json"

SERVICE_HOSTS = {
    "pypi":    ["pypi.org", "files.pythonhosted.org"],
    "github":  ["github.com", "raw.githubusercontent.com", "codeload.github.com"],
    "httpbin": ["httpbin.org"],
}

DEFAULT_STATE = {
    "kill_all": False,
    "services": {k: True for k in SERVICE_HOSTS},
}


def _load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return DEFAULT_STATE


def request(flow: http.HTTPFlow) -> None:
    state = _load_state()
    host = flow.request.pretty_host

    if state.get("kill_all"):
        flow.response = http.Response.make(
            503,
            b"[Workshop proxy] All external services disabled.",
            {"Content-Type": "text/plain"},
        )
        return

    services = state.get("services", {})
    for key, hostnames in SERVICE_HOSTS.items():
        if not services.get(key, True):
            if any(h in host for h in hostnames):
                flow.response = http.Response.make(
                    503,
                    f"[Workshop proxy] Service '{key}' is currently disabled.".encode(),
                    {"Content-Type": "text/plain"},
                )
                return
