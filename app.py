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

st.set_page_config(page_title="DENKO-MASTER OS", layout="centered")

# セッション状態の初期化
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'idx' not in st.session_state: st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
if 'show_exp' not in st.session_state: st.session_state.show_exp = False

# CSSでスマホ向けにさらに最適化
st.markdown("""
    <style>
    .main { background-color: #111; color: #eee; }
    .stButton>button { width: 100%; height: 4em; font-size: 1.2rem; background-color: #28a745; color: white; border-radius: 10px; }
    .stRadio > label { font-size: 1.2rem !important; font-weight: bold; color: #00FF00; }
    /* スコア表示用のスタイル */
    .score-container { background-color: #222; padding: 10px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 電気工事士：一発合格特化")

# --- スマホ対応：スコアを最上部に表示 ---
if st.session_state.total > 0:
    acc = int(st.session_state.score / st.session_state.total * 100)
    st.markdown(f"""
    <div class="score-container">
        <b>現在の戦績: {st.session_state.score} / {st.session_state.total} 問正解 ({acc}%)</b>
    </div>
    """, unsafe_allow_html=True)
else:
    st.write("まずは1問解いてみよう。")

st.write(f"現在弾薬庫に装填中: {len(MASTER_QUESTIONS)} 問")

if not MASTER_QUESTIONS:
    st.error("弾薬庫(questions.json)が見つかりません。")
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
            st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
            st.session_state.show_exp = False
            st.rerun()

# サイドバーは一応残すが、メイン画面でも完結させる
st.sidebar.metric("正解数", f"{st.session_state.score} / {st.session_state.total}")
if st.sidebar.button("スコアをリセット"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.rerun()
