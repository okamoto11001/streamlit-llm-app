from dotenv import load_dotenv

load_dotenv()

import os
from flask import Flask, render_template_string, request
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

app = Flask(__name__)

# --- LangChain LLM セットアップ（Lesson8準拠） ---
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# --- 専門家プロンプト定義 ---
EXPERT_SYSTEM_PROMPTS = {
    "medical": "あなたは医療の専門家です。健康・病気・生活習慣に関する専門的かつ安全なアドバイスを提供してください。",
    "law": "あなたは法律の専門家です。一般的な法的情報を提供し、危険な助言を避けつつ丁寧に説明してください。",
    "programming": "あなたはプログラミングの講師です。初心者にも分かりやすく、丁寧にコードや概念を解説してください。"
}

# --- 引数（入力テキスト・専門家タイプ） → LLM回答 を返す関数 ---
def run_llm(user_input: str, expert_type: str) -> str:
    system_prompt = EXPERT_SYSTEM_PROMPTS.get(expert_type, "You are a helpful assistant.")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    result = llm(messages)
    return result.content


# --- HTML（入力フォーム＋説明文＋結果表示） ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>LangChain LLM Demo</title>
</head>
<body>
    <h2>LangChain × LLM Webアプリ</h2>
    <p>
        ここでは、入力フォームに質問を入力し、下のラジオボタンで<br>
        「どの専門家として回答するか」を選択できます。<br>
        送信すると、選択した専門家の観点でLLMが回答を返します。
    </p>

    <form method="POST">

        <h3>■ 専門家の種類を選択してください</h3>
        <label><input type="radio" name="expert" value="medical" checked> 医療アドバイザー</label><br>
        <label><input type="radio" name="expert" value="law"> 法律アドバイザー</label><br>
        <label><input type="radio" name="expert" value="programming"> プログラミング講師</label><br><br>

        <h3>■ 質問内容を入力</h3>
        <input type="text" name="user_input" placeholder="質問を入力してください" style="width:400px">
        <button type="submit">送信</button>
    </form>

    {% if result %}
        <h3>回答：</h3>
        <div style="white-space: pre-wrap; border:1px solid #ccc; padding:10px; width:500px;">
            {{ result }}
        </div>
    {% endif %}
</body>
</html>
"""

# --- Flask ルーティング ---
@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None

    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        expert_type = request.form.get("expert", "medical")

        # ここで関数を利用
        result_text = run_llm(user_input, expert_type)

    return render_template_string(HTML_TEMPLATE, result=result_text)


# --- 実行 ---
if __name__ == "__main__":
    app.run(debug=True)