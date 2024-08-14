import json
from pathlib import Path
from flask import Flask, request, render_template, Markup, redirect, url_for

from src.config import Config
from src.chat.session import single_turn_interaction


app = Flask(__name__, template_folder='templates')
app.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY

chat_histories = {}
chat_sessions = {}


def load_contexts():
    db_file = Config.DATA_DIR / "task_theory_part_1_db.json"
    with open(db_file, 'r') as f:
        return json.load(f)


@app.route('/', methods=['GET'])
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    session_id = request.args.get('session_id')
    
    if not session_id:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        contexts = load_contexts()
        response = single_turn_interaction(user_input, contexts, Config.INSTRUCTION_TEMPLATE)
        response_html = Markup(response.replace("\n", "<br>"))
        
        chat_histories.setdefault(session_id, []).append({
            "message": user_input,
            "class": "user-msg"
        })
        chat_histories[session_id].append({
            "message": response_html,
            "class": "bot-msg"
        })
    
    return render_template('chat.html', chat_histories=chat_histories, session_id=session_id, request=request)


def main():
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=True)


if __name__ == '__main__':
    main()

