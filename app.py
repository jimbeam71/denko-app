import streamlit as st
import random
import json
import os

# 弾薬庫(questions.json)から問題をロード
def load_data():
    if os.path.exists("questions.json"):
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

MASTER_QUESTIONS = load_data()

st.set_page_config(page_title="DENKO-MASTER HIGH-CONTRAST", layout="centered")

# セッション状態の初期化
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'idx' not in st.session_state:
    if MASTER_QUESTIONS:
        st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
if 'show_exp' not in st.session_state: st.session_state.show_exp = False

# --- 超高コントラストCSS：白文字と巨大ボタン ---
st.markdown("""
    <style>
    /* 全体背景と基本文字色（完全な白） */
    .main { background-color: #000000; color: #ffffff !important; }
    
    /* モバイル用戦況モニター：背景をグレーにして文字を白に強調 */
    .mobile-score {
        background-color: #222222;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffffff;
        margin-bottom: 25px;
        text-align: center;
    }
    .score-text { font-size: 1.8rem; font-weight: bold; color: #ffffff !important; }
    .acc-text { font-size: 1.1rem; color: #00FF00 !important; font-weight: bold; }

    /* 問題文と選択肢の文字を大きく、白く */
    h3, p, label, .stMarkdown { color: #ffffff !important; font-size: 1.2rem !important; }
    
    /* 選択肢のラジオボタンの文字（白） */
    .stRadio > label { font-size: 1.3rem !important; font-weight: bold !important; color: #ffffff !important; }
    div[role="radiogroup"] label { color: #ffffff !important; }

    /* 解答ボタン：巨大かつ高輝度 */
    .stButton>button {
        width: 100%;
        height: 5em;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        background-color: #28a745 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 20px !important;
    }

    /* 成功・エラーメッセージの視認性向上 */
    .stAlert { font-size: 1.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 電気工事士：一発合格特化")

# --- 戦況モニター（最上部固定） ---
if st.session_state.total > 0:
    acc = int(st.session_state.score / st.session_state.total * 100)
    st.markdown(f"""
    <div class="mobile-score">
        <div class="score-text">正解数: {st.session_state.score} / {st.session_state.total}</div>
        <div class="acc-text">現在の命中率: {acc}%</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="mobile-score"><div class="score-text" style="font-size:1.2rem;">問題を解いて戦績を表示せよ</div></div>', unsafe_allow_html=True)

if not MASTER_QUESTIONS:
    st.error("弾薬庫(questions.json)が見つかりません。")
else:
    q = MASTER_QUESTIONS[st.session_state.idx]
    
    # ジャンル表示
    is_hack = "【計算ハック】" in q['q']
    genre_label = "🔴 【計算問題】" if is_hack else "🔵 【暗記問題】"
    st.markdown(f"**カテゴリー: {genre_label}**")
    
    st.markdown(f"### {q['q']}")
    
    # 選択肢表示（キーにインデックスを含めて重複回避）
    choice = st.radio("選択肢を狙撃せよ:", q['o'], key=f"q_{st.session_state.idx}")

    # 解答照合
    if st.button("解答を確認 (CHECK)"):
        if not st.session_state.show_exp:
            st.session_state.total += 1
            if choice == q['a']:
                st.success("🎯 撃破（正解）！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 被弾（不正解）。正解は [{q['a']}]")
            st.session_state.show_exp = True

    # 解説と次へ
    if st.session_state.show_exp:
        st.info(f"**【NOM-OS解析】**\n\n{q['exp']}")
        if st.button("次の標的へ (NEXT)"):
            # 40%で計算、60%で暗記の重み付けランダム
            hacks = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" in quest['q']]
            others = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" not in quest['q']]
            
            if random.random() < 0.4 and hacks:
                st.session_state.idx = random.choice(hacks)
            else:
                st.session_state.idx = random.choice(others)
                
            st.session_state.show_exp = False
            st.rerun()

# 予備：サイドバーのリセットボタン
with st.sidebar:
    if st.button("戦績をリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()
