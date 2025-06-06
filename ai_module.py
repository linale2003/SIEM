from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk

# Подключение к Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Ключевые слова, при которых считаем лог "Опасным"
danger_keywords = ["failed", "unauthorized", "error", "invalid", "denied", "refused"]

def analyze_log(message):
    msg_lower = message.lower()
    for keyword in danger_keywords:
        if keyword in msg_lower:
            return "Опасно"
    return "Окей"

def tag_logs():
    index_name = "siem-logs"
    docs = scan(es, index=index_name, query={"query": {"match_all": {}}})

    actions = []

    for doc in docs:
        doc_id = doc["_id"]
        message = doc["_source"].get("message", "")

        tag = analyze_log(message)

        action = {
            "_op_type": "update",
            "_index": index_name,
            "_id": doc_id,
            "doc": {
                "ai_tag": tag
            }
        }
        actions.append(action)

    if actions:
        bulk(es, actions)
        print(f"✅ Добавлены метки в {len(actions)} логов.")
    else:
        print("❗ Логи не найдены.")

if __name__ == "__main__":
    tag_logs()
