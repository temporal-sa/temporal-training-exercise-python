"""
ABOUTME: Flask control panel for the workshop network proxy.
Reads and writes /root/proxy/state.json. Served on port 5000.

Ported from temporal-sa/ai-agents-webinar. Flipping a toggle off makes
mitmproxy return HTTP 503 for that service's hosts on the next request, with
no restart. `kill_all` overrides every individual toggle.
"""
import json
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="/root/proxy/static")
STATE_FILE = "/root/proxy/state.json"

DEFAULT_STATE = {
    "kill_all": False,
    "services": {
        "pypi": True,
        "github": True,
        "httpbin": True,
    },
}

SERVICE_LABELS = {
    "pypi":    "Python Package Index  (pypi.org)",
    "github":  "GitHub  (github.com)",
    "httpbin": "HTTP echo  (httpbin.org)",
}


def read_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return dict(DEFAULT_STATE)


def write_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


@app.route("/")
def index():
    return send_from_directory("/root/proxy/static", "index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify(read_state())


@app.route("/api/state", methods=["POST"])
def set_state():
    state = request.get_json(force=True)
    write_state(state)
    return jsonify({"ok": True})


@app.route("/api/service/<key>", methods=["POST"])
def toggle_service(key):
    data = request.get_json(force=True)
    state = read_state()
    state.setdefault("services", {})[key] = bool(data.get("enabled", True))
    write_state(state)
    return jsonify({"ok": True, "key": key, "enabled": state["services"][key]})


@app.route("/api/kill_all", methods=["POST"])
def kill_all():
    data = request.get_json(force=True)
    state = read_state()
    state["kill_all"] = bool(data.get("enabled", False))
    write_state(state)
    return jsonify({"ok": True, "kill_all": state["kill_all"]})


@app.route("/api/labels", methods=["GET"])
def labels():
    return jsonify(SERVICE_LABELS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
