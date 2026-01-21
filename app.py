import streamlit as st
import google.generativeai as genai

# --- ページ設定 ---
st.set_page_config(
    page_title="Event Planner AI",
    page_icon="🎤",
    layout="wide"
)

# カスタムCSSでデザインを調整
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .output-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APIキーの設定 ---
# Web公開時は Streamlitの管理画面(Secrets)に登録することを推奨
API_KEY = st.sidebar.text_input("Gemini API Key", type="password")

if not API_KEY:
    st.warning("左側のサイドバーに Gemini APIキーを入力してください。")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- メインコンテンツ ---
st.title("🎤 イベント企画案 生成アシスタント")
st.caption("登壇者の情報をリサーチし、最適なイベントプランをGeminiが提案します。")

# --- STEP 1: 登壇者リサーチ ---
with st.container():
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        speaker_name = st.text_input("👤 登壇者氏名", placeholder="氏名を入力")
    
    if speaker_name:
        with st.spinner("登壇者の情報を確認中..."):
            res_research = model.generate_content(f"{speaker_name}氏の専門分野と特徴を、企画立案の参考になるように150文字程度で要約してください。")
            st.info(f"**【登壇者プロフィール（AI抽出）】**\n\n{res_research.text}")

st.divider()

# --- STEP 2: 企画入力と出力 ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📝 企画の種（入力）")
    with st.expander("入力を開始する", expanded=True):
        theme = st.text_input("◆テーマ（タイトル）")
        purpose = st.text_area("◆イベントの目的")
        target = st.text_area("◆ターゲット参加者")
        transformation = st.text_area("◆ターゲットの行動変容")
        benefit = st.text_area("◆ご登壇者のベネフィット")
        content = st.text_area("◆講演内容")
        method = st.radio("◆講演方法", ["講演", "パネルディスカッション", "セミナー", "ワークショップ"], horizontal=True)
        
        generate_btn = st.button("Geminiで企画案を生成する →")

with col_right:
    st.subheader("✨ 生成された企画構成案")
    if generate_btn:
        with st.spinner("企画を練り上げています..."):
            prompt = f"""
            あなたはプロのイベントプロデューサーです。
            登壇者の特性「{speaker_name}」を最大限に活かし、参加者の満足度が高いイベント案を作成してください。

            【元の入力情報】
            テーマ: {theme} / 目的: {purpose} / ターゲット: {target} / 変化: {transformation} / 特典: {benefit} / 内容: {content} / 方法: {method}

            【出力形式】
            以下のフォーマットで出力してください。
            ---
            【企画構成案】
            ◆テーマ（タイトル）
            ＜魅力的なタイトル案＞

            ◆イベントの目的
            ＜整理された目的＞

            ◆ターゲット参加者
            ＜具体的なターゲット像＞

            ◆ターゲットの行動変容（どんな状態になって欲しいか）
            ＜終了後の理想的な状態＞

            ◆ご登壇者のベネフィット
            ＜登壇者にとってのメリット＞

            ◆講演内容
            ＜登壇者の強みを反映した具体的な構成案＞

            ◆講演方法
            {method}

            ◆タイムスケジュール
            19:00～19:05　クラブの紹介＆オープニング
            19:05～20:00　講演会
            20:00～20:20　質疑応答
            20:20～20:30　締め　その後懇親会
            ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
            20:30～23:00　懇親会
            """
            response = model.generate_content(prompt)
            st.markdown(f'<div class="output-box">{response.text}</div>', unsafe_allow_html=True)
            st.download_button("テキスト形式で保存", response.text, file_name="event_plan.txt")
    else:
        st.info("左側のフォームを埋めて、生成ボタンを押してください。")
