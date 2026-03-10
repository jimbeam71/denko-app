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

# アプリ設定
st.set_page_config(page_title="DENKO-MASTER FORCE", layout="centered")

# セッション状態の初期化
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'idx' not in st.session_state:
    if MASTER_QUESTIONS:
        st.session_state.idx = random.randint(0, len(MASTER_QUESTIONS)-1)
if 'show_exp' not in st.session_state: st.session_state.show_exp = False

# --- 【超強力】全デバイス強制ダークモードCSS ---
st.markdown("""
    <style>
    /* 全体の背景を真っ黒に、文字を真っ白に固定 */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* 全テキスト要素を白に強制 */
    h1, h2, h3, p, span, label, div {
        color: #ffffff !important;
    }

    /* 戦況モニター（背景を濃いグレーにして白文字を浮かせる） */
    .mobile-score {
        background-color: #222222 !important;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffffff;
        margin-bottom: 25px;
        text-align: center;
    }
    .score-text { 
        font-size: 1.8rem; 
        font-weight: bold; 
        color: #ffffff !important; 
    }
    .acc-text { 
        font-size: 1.1rem; 
        color: #00FF00 !important; 
        font-weight: bold; 
    }

    /* ラジオボタン（選択肢）の文字を大きく、白く */
    [data-testid="stMarkdownContainer"] p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
    }
    
    /* 巨大な解答ボタン */
    .stButton>button {
        width: 100% !important;
        height: 5em !important;
        background-color: #28a745 !important;
        color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 20px !important;
    }

    /* 成功・警告メッセージの枠を調整 */
    .stAlert {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ 電気工事士：一発合格特化")

# --- 戦況モニター ---
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
    
    # カテゴリー表示
    is_hack = "【計算ハック】" in q['q']
    genre_label = "🔴 計算問題" if is_hack else "🔵 暗記問題"
    st.markdown(f"**カテゴリー: {genre_label}**")
    
    # 問題文
    st.markdown(f"### {q['q']}")
    
    # 選択肢
    choice = st.radio("選択肢を狙撃せよ:", q['o'], key=f"q_{st.session_state.idx}")

    # 解答ボタン
    if st.button("解答を確認 (CHECK)"):
        if not st.session_state.show_exp:
            st.session_state.total += 1
            if choice == q['a']:
                st.success("🎯 正解！完璧だ。")
                st.session_state.score += 1
            else:
                st.error(f"❌ 不正解。正解は [{q['a']}]")
            st.session_state.show_exp = True

    # 解説と次へ
    if st.session_state.show_exp:
        st.info(f"**【覚え方】**\n\n{q['exp']}")
        if st.button("次の標的へ (NEXT)"):
            hacks = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" in quest['q']]
            others = [i for i, quest in enumerate(MASTER_QUESTIONS) if "【計算ハック】" not in quest['q']]
            
            if random.random() < 0.4 and hacks:
                st.session_state.idx = random.choice(hacks)
            else:
                st.session_state.idx = random.choice(others)
                
            st.session_state.show_exp = False
            st.rerun()

with st.sidebar:
    if st.button("戦績をリセット"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()
