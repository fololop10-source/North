from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)
DB_FILE = "chat_data.txt"

# Функция для загрузки сообщений
def get_messages():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return [eval(line) for line in f.readlines()]

# Код страницы (С авто-обновлением каждые 3 секунды)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>NORTH MESSENGER</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0b0e11; color: #e9edef; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .header { color: #00a884; margin: 15px 0; font-size: 24px; font-weight: bold; text-transform: uppercase; }
        #chat { width: 90%; max-width: 500px; height: 65vh; overflow-y: auto; background: #111b21; border-radius: 12px; padding: 10px; border: 1px solid #222e35; }
        .m { background: #202c33; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #00a884; word-wrap: break-word; }
        .u { color: #00a884; font-weight: bold; margin-right: 5px; }
        .input-area { width: 90%; max-width: 500px; margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        input { background: #2a3942; border: none; padding: 12px; color: white; border-radius: 8px; outline: none; }
        button { background: #00a884; color: #111b21; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">NORTH</div>
    <div id="chat"></div>
    <div class="input-area">
        <input type="text" id="user" placeholder="Ваш ник" maxlength="15">
        <input type="text" id="text" placeholder="Сообщение...">
        <button onclick="send()">ОТПРАВИТЬ</button>
    </div>

    <script>
        async function load() {
            let r = await fetch('/api/get');
            let msgs = await r.json();
            let div = document.getElementById('chat');
            let wasAtBottom = div.scrollHeight - div.clientHeight <= div.scrollTop + 1;
            div.innerHTML = msgs.map(m => `<div class="m"><span class="u">${m.u}:</span>${m.t}</div>`).join('');
            if (wasAtBottom) div.scrollTop = div.scrollHeight;
        }
        async function send() {
            let u = document.getElementById('user').value;
            let t = document.getElementById('text').value;
            if(!u || !t) return;
            await fetch('/api/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: `u=${encodeURIComponent(u)}&t=${encodeURIComponent(t)}`
            });
            document.getElementById('text').value = '';
            load();
        }
        setInterval(load, 3000); // Обновлять каждые 3 секунды
        load();
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/api/get')
def get_api(): return jsonify(get_messages())

@app.route('/api/send', methods=['POST'])
def send_api():
    u, t = request.form.get('u'), request.form.get('t')
    if u and t:
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(str({'u': u, 't': t}) + "\\n")
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
