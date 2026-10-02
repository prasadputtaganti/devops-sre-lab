from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "application": "devops-sre-demo",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "status": "healthy"
    }

@app.route("/health")
def health():
    return {"status": "UP"}

@app.route("/ready")
def ready():
    return {"status": "READY"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
