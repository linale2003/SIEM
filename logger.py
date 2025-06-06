from flask import Flask, request
from elasticsearch import Elasticsearch
from datetime import datetime

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "siem-logs"

@app.route("/log", methods=["POST"])
def receive_log():
    data = request.json
    log_doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "host": data.get("host"),
        "event": data.get("log"),
        "source": "agent"
    }
    es.index(index=INDEX_NAME, body=log_doc)
    print(f"✅ Получено: {log_doc}")
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)