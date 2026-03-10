import streamlit as st
import random
import json
import os

# 弾薬庫(questions.json)から問題をロードする
def load_data():
    if os.path.exists("questions.json"):
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

MASTER_QUESTIONS = load_data()

st.set_page_config(page_title="NOM-OS ARSENAL", layout="centered")

if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'idx' not in st.session_state: st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
if 'show_exp' not in st.session_state: st.session_state.show_exp = False

st.markdown("""
    <style>
    .main { background-color: #111; color: #eee; }
    .stButton>button { width: 100%; height: 4em; font-size: 1.2rem; background-color: #28a745; color: white; border-radius: 10px; }
    .stRadio > label { font-size: 1.2rem !important; font-weight: bold; color: #00FF00; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 電気工事士：一発合格特化ユニット")
st.write(f"現在弾薬庫に装填中: {len(MASTER_QUESTIONS)} 問")

if not MASTER_QUESTIONS:
    st.error("弾薬庫(questions.json)が空、または存在しません。")
else:
    q = MASTER_QUESTIONS[st.session_state.idx]
    st.markdown(f"--- \n ### **問題:**\n{q['q']}")
    choice = st.radio("選択肢を選べ:", q['o'], key=f"q_{st.session_state.idx}")

    if st.button("解答をチェックする"):
        st.session_state.total += 1
        if choice == q['a']:
            st.success("🎯 正解！完璧だ。")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解（正解は: {q['a']}）")
        st.session_state.show_exp = True

    if st.session_state.show_exp:
        st.warning(f"**【合格への覚え方】**\n{q['exp']}")
        if st.button("次の問題へ進む"):
            # ここで完全にランダムに次の問題を選ぶ
            st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
            st.session_state.show_exp = False
            st.rerun()

st.sidebar.metric("正解数", f"{st.session_state.score} / {st.session_state.total}")
if st.session_state.total > 0:
    st.sidebar.write(f"正答率: {int(st.session_state.score/st.session_state.total*100)}%")