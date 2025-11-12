from flask import Flask, request
from pathlib import Path
import subprocess, hmac, hashlib, os

SECRET = os.getenv("WEBHOOK_SECRET", "devsecret").encode()

def find_repo_root(start=None):
    path = Path(start or __file__).resolve()
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("No .git directory found")

REPO_PATH = find_repo_root()

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    sig = request.headers.get("X-Hub-Signature-256")
    body = request.data
    expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return "Forbidden", 403

    if request.headers.get("X-GitHub-Event") == "push":
        subprocess.run(["git", "-C", REPO_PATH, "fetch", "--all"])
        subprocess.run(["git", "-C", REPO_PATH, "reset", "--hard", "origin/main"])
        subprocess.run(["systemctl", "restart", "smallsentry"])
        return "Updated SmallSentry", 200
    return "Ignored", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
