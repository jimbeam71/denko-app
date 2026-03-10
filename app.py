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

st.set_page_config(page_title="DENKO-MASTER HYBRID", layout="centered")

# セッション状態の初期化
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'idx' not in st.session_state:
    # 起動時の最初の一問をセット
    st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
if 'show_exp' not in st.session_state: st.session_state.show_exp = False

# CSS設定
st.markdown("""
    <style>
    .main { background-color: #111; color: #eee; }
    .stButton>button { width: 100%; height: 4em; font-size: 1.2rem; background-color: #28a745; color: white; border-radius: 10px; }
    .stRadio > label { font-size: 1.2rem !important; font-weight: bold; color: #00FF00; }
    .score-container { background-color: #222; padding: 10px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 電気工事士：一発合格特化")

# スコアを最上部に表示（スマホ対応）
if st.session_state.total > 0:
    acc = int(st.session_state.score / st.session_state.total * 100)
    st.markdown(f'<div class="score-container"><b>現在の戦績: {st.session_state.score} / {st.session_state.total} 問正解 ({acc}%)</b></div>', unsafe_allow_html=True)

if not MASTER_QUESTIONS:
    st.error("弾薬庫(questions.json)が見つかりません。")
else:
    # 現在の問題を取得
    q = MASTER_QUESTIONS[st.session_state.idx]
    
    # ジャンル表示の最適化
    genre = "【計算問題】" if "【計算ハック】" in q['q'] else "【暗記問題】"
    st.write(f"ジャンル: {genre}")
    
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
            # --- 戦略的ランダム・ロジック ---
            # 計算問題と暗記問題を分離
            hacks = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" in quest['q']]
            others = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" not in quest['q']]
            
            # 40%の確率で計算問題、60%の確率で暗記問題を出すように重み付け
            if random.random() < 0.4 and hacks:
                st.session_state.idx = random.choice(hacks)
            else:
                st.session_state.idx = random.choice(others)
                
            st.session_state.show_exp = False
            st.rerun()

st.sidebar.metric("正解数", f"{st.session_state.score} / {st.session_state.total}")
if st.sidebar.button("スコアをリセット"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.rerun()
