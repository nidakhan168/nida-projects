import os
from datetime import datetime

from flask import Flask, render_template_string, request
from chatbot_core import ChemLabBuddy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("/Users/siddiqkhan/Downloads/CHEMLAB BUDDY/data/chem_faq.csv")))
FAQ_PATH = os.path.join(BASE_DIR, "data", "chem_faq.csv")
LOG_PATH = os.path.join(BASE_DIR, "logs", "unknown_questions.log") 

app = Flask(__name__)
bot = ChemLabBuddy(FAQ_PATH)

def log_unknown_question(question: str, score: float) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | score={score:.3f} | {question}\n")

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>ChemLabBuddy Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; }
    .chat-box { border: 1px solid #ccc; padding: 20px; border-radius: 8px; }
    .msg-user { text-align: right; margin: 10px 0; }
    .msg-bot { text-align: left; margin: 10px 0; }
    .bubble { display: inline-block; padding: 10px 14px; border-radius: 16px; max-width: 80%; }
    .user-bubble { background: #007bff; color: white; }
    .bot-bubble { background: #f1f1f1; }
    form { margin-top: 20px; display: flex; gap: 10px; }
    input[type=text] { flex: 1; padding: 8px; }
    button { padding: 8px 16px; }
  </style>
</head>
<body>
  <h1>🧪 ChemLabBuddy</h1>
  <p>A simple chemistry lab assistant chatbot (Python + NLP).</p>
  <div class="chat-box">
    {% for entry in chat_history %}
      {% if entry.role == 'user' %}
        <div class="msg-user">
          <div class="bubble user-bubble">{{ entry.text }}</div>
        </div>
      {% else %}
        <div class="msg-bot">
          <div class="bubble bot-bubble">{{ entry.text }}</div>
        </div>
      {% endif %}
    {% endfor %}
  </div>

  <form method="POST">
    <input type="text" name="user_input" placeholder="Ask a chemistry question..." autofocus required>
    <button type="submit">Send</button>
  </form>
</body>
</html>
"""

chat_history = [
    {"role": "bot", "text": "Hi, I'm ChemLabBuddy. Ask me about solutions, titrations, stoichiometry, gas laws, or safety!"}
]


@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            chat_history.append({"role": "user", "text": user_input})
            answer, topic, score = bot.get_answer(user_input)

            if answer is None:
                bot_text = (
                    "I'm not sure about that yet. "
                    "Please check your lab manual or supervisor."
                )
                log_unknown_question(user_input, score)
            else:
                bot_text = f"[{topic}, match={score:.2f}] {answer}"

            chat_history.append({"role": "bot", "text": bot_text})

    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)


if __name__ == "__main__":
    app.run(debug=True)
