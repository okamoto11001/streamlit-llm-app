from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

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
    "programming": "あなたはプログラミングの講師です。初心者にも分かりやすくコードや概念を解説してください。"
}

# --- 入力テキスト＋選択専門家 → LLM回答 を返す関数 ---
def run_llm(user_input: str, expert_type: str) -> str:
    system_prompt = EXPERT_SYSTEM_PROMPTS.get(expert_type, "You are a helpful assistant.")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input),
    ]

    result = llm(messages)
    return result.content


# --- Streamlit UI ---
st.title("LangChain × LLM Webアプリ（Streamlit版）")

st.write("""
ここでは、 **入力フォームに質問を入力** し、  
**ラジオボタンで回答する専門家の種類を選択** できます。

「送信」ボタンを押すと、選択した専門家として LLM が回答します。
""")

# ラジオボタン（専門家選択）
expert_type = st.radio(
    "■ 専門家の種類を選択してください",
    options={
        "medical": "医療アドバイザー",
        "law": "法律アドバイザー",
        "programming": "プログラミング講師"
    }
)

# 入力フォーム
user_input = st.text_input("■ 質問内容を入力してください", "")

# ボタンで LLM 実行
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("LLMに問い合わせ中..."):
            result = run_llm(user_input, expert_type)
        st.subheader("回答：")
        st.write(result)
