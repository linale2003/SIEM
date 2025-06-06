import time
import socket
import requests

LOG_FILE = "/var/log/auth.log"
SIEM_SERVER = "http://10.10.11.100:5000/log"  # IP сервера SIEM с логгером

hostname = socket.gethostname()

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

with open(LOG_FILE, "r") as f:
    for line in follow(f):
        data = {
            "host": hostname,
            "log": line.strip()
        }
        try:
            requests.post(SIEM_SERVER, json=data)
            print(f"📤 Отправлено: {data}")
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")