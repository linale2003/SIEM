from flask import Flask, request, jsonify
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

@app.route("/api/logs", methods=["GET"])
def get_logs():
    try:
        res = es.search(index=INDEX_NAME, size=50, sort="timestamp:desc")
        logs = [
            {
                "timestamp": hit["_source"].get("timestamp"),
                "host": hit["_source"].get("host"),
                "event": hit["_source"].get("event"),
                "ai_tag": hit["_source"].get("ai_tag", "—")
            }
            for hit in res["hits"]["hits"]
        ]
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
