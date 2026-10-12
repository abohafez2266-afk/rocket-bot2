import requests, time, random, datetime, threading
from flask import Flask
TOKEN = "8798093799:AAGmQs1Vvk6PgJtHA13ocCrI40BBhM05C-k"
BASE = f"https://api.telegram.org/bot{TOKEN}"
app = Flask(__name__)
@app.route('/')
def home(): return "ROCKET PRO 24h"
pairs = ["CAD/JPY OTC", "EUR/USD OTC", "GBP/JPY OTC", "EUR/JPY OTC", "USD/JPY OTC"]
chat_ids = set()
last_update = 0
def make_signal():
    pair = random.choice(pairs)
    direction = random.choice(["BUY UP", "SELL DOWN"])
    payout = random.randint(88, 95)
    now = datetime.datetime.now()
    return f"ROCKET PRO SIGNAL\nPair: {pair}\nSignal: {direction}\nPayout: {payout}%\nTime: {now.strftime('%H:%M:%S')}\nFrame: M1"
def auto_sender():
    while True:
        time.sleep(180)
        if not chat_ids: continue
        sig = make_signal()
        for cid in list(chat_ids):
            try: requests.get(f"{BASE}/sendMessage", params={"chat_id": cid, "text": sig}, timeout=10)
            except: pass
def bot_loop():
    global last_update
    requests.get(f"{BASE}/deleteWebhook?drop_pending_updates=True", timeout=10)
    while True:
        try:
            r = requests.get(f"{BASE}/getUpdates", params={"offset": last_update+1, "timeout": 20}, timeout=25).json()
            for u in r.get("result", []):
                last_update = u["update_id"]
                if "message" not in u: continue
                cid = u["message"]["chat"]["id"]
                text = u["message"].get("text","").lower()
                chat_ids.add(cid)
                if "/start" in text:
                    requests.get(f"{BASE}/sendMessage", params={"chat_id": cid, "text": "Ready! Bot 24h - signal every 3 min"}, timeout=10)
                elif "signal" in text or "اشارة" in text:
                    requests.get(f"{BASE}/sendMessage", params={"chat_id": cid, "text": make_signal()}, timeout=10)
        except: time.sleep(3)
threading.Thread(target=bot_loop, daemon=True).start()
threading.Thread(target=auto_sender, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
