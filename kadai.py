import streamlit as st
import requests
import time
from datetime import datetime
import os


# ----- 設定 -----
st.set_page_config(page_title="朝の準備サポート", page_icon="🌅")
st.title("☀朝の準備サポートアプリ")

st.markdown("---")
# ----- 1. 天気取得と服装提案 -----
st.header("☁️ 今日の天気 & 服装提案")

city = st.text_input("都市名を入力してください（例: Tokyo, Osaka, Sapporo）")

api_key = os.getenv("SECRET_API")

if st.button("天気を確認！"):
    if city.strip() == "":
        st.warning("都市名を入力してください。")
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={api_key}&units=metric&lang=ja"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]

            st.success(f"🌡 現在の気温: {temp}℃\n\n☁️ 天気: {weather}")

            st.subheader("👕 今日のおすすめ服装")
            # 服装画像と説明のペア
            if temp < 10:
                st.image("https://cancam.jp/wp-content/uploads/2018/12/25/219.jpg", caption="厚手のコートがおすすめです。暖かくしてくださいね！")
            elif temp < 20:
                st.image("https://cancam.jp/wp-content/uploads/2019/10/30/214.jpg", caption="薄手のジャケットがちょうど良いでしょう。")
            else:
                st.image("https://img-more.hpplus.jp/w=952,q=75,a=0,f=webp:auto,through=gif/image/b0/b0805928-995b-45b8-b919-eaa2e82f5259-2048x1152.jpg", caption="Tシャツで快適です！")

        else:
            st.error("天気情報を取得できませんでした。都市名やAPIキーを確認してください。")
st.markdown("---")
# ----- 2. 食材から朝食メニュー提案＆カロリー計算（チェックボックス形式） -----
st.header("🍳 食材から朝食メニュー提案＆カロリー計算")

menu_dict = {
    "卵": ["オムレツ", "ゆで卵サラダ", "スクランブルエッグ"],
    "トマト": ["トマトサラダ", "カプレーゼ", "トマトスープ"],
    "鶏肉": ["チキンソテー", "鶏の照り焼き", "鶏肉サラダ"],
    "パン": ["トースト", "サンドイッチ", "フレンチトースト"],
    "アボカド": ["アボカドトースト", "アボカドサラダ"],
    "ヨーグルト": ["ヨーグルトとフルーツ", "ヨーグルトパフェ"],
    "ベーコン": ["ベーコン＆エッグ", "ベーコン炒め"],
    "バナナ": ["バナナスムージー", "バナナパンケーキ"]
}

calorie_dict = {
    "卵": 150,
    "トマト": 20,
    "鶏肉": 200,
    "パン": 250,
    "アボカド": 160,
    "ヨーグルト": 60,
    "ベーコン": 300,
    "バナナ": 90
}

st.write("お持ちの材料を選択してください：")
selected_items = []
cols = st.columns(4)
ingredients = list(menu_dict.keys())

for i, item in enumerate(ingredients):
    with cols[i % 4]:
        if st.checkbox(item):
            selected_items.append(item)

if st.button("メニュー提案＆カロリー計算"):
    if not selected_items:
        st.warning("材料を1つ以上選んでください。")
    else:
        possible_menus = set()
        total_calorie = 0

        for item in selected_items:
            possible_menus.update(menu_dict.get(item, []))
            total_calorie += calorie_dict.get(item, 0)

        st.subheader("🧑‍🍳 おすすめメニュー:")
        for menu in sorted(possible_menus):
            st.write(f"- {menu}")

        st.write(f"🔥 推定カロリー合計（100g換算合計）: {total_calorie} kcal")
st.markdown("---")
# ----- 3. モチベーション動画（JSON管理） -----
st.header("🎬 モチベーション動画")
video_data = {
    "元気が欲しい": [
        {"title": "【洋楽】ハッピーな気持ちのスイッチが入るポップで可愛い洋楽プレイリスト", "url": "https://www.youtube.com/watch?v=1O3o_c4a-J4"}
    ],
    "集中したい": [
        {"title": "Lo-fi作業用BGM", "url": "https://www.youtube.com/watch?v=5qap5aO4i9A"}
    ],
    "リラックスしたい": [
        {"title": "おはようジブリ＆ディズニー", "url": "https://www.youtube.com/watch?v=5GM1UrRGX3c&t=39s"}
    ],
    "おしゃな雰囲気に浸りたい": [
        {"title": "朝準備する時にかけ流したいお洒落でテンション上がる曲集", "url": "https://www.youtube.com/watch?v=ZC9hcDNaZBc&t=29s"}
    ],
    "プリンセスになりたい": [
        {"title": "朝プリンセスになれるPlaylist", "url": "https://www.youtube.com/watch?v=9IBUcS4SGQ0"}
    ]
}

mood = st.selectbox("今の気分は？", list(video_data.keys()))
for video in video_data[mood]:
    st.subheader(video["title"])
    st.video(video["url"])

st.markdown("---")
# ----- 4. タイマーと進行バー（分単位） -----
st.header("⏰ タイマーで準備をサポート！")

duration_min = st.slider("準備にかける時間（分）を選んでください", min_value=1, max_value=10, step=1)

if st.button("スタート！"):
    st.write(f"🕒 タイマー開始：{duration_min}分")
    progress_bar = st.progress(0)
    timer_placeholder = st.empty()
    total_seconds = duration_min * 60

    for i in range(total_seconds):
        remaining = total_seconds - i
        mins = remaining // 60
        secs = remaining % 60
        timer_placeholder.write(f"残り時間: {mins}分 {secs}秒")
        progress_bar.progress(i / total_seconds)
        time.sleep(1)

    timer_placeholder.write("✅ タイムアップ！準備完了！")
    st.balloons()

st.markdown("---")
# ----- 5. 今日の予定表示（フォーム入力、変更なし） -----
st.header("📅 今日の予定")

with st.form("schedule_form"):
    today_date = datetime.today().strftime('%Y-%m-%d')
    st.write(f"日付：{today_date}")
    tasks = st.text_area("今日の予定を入力してください（1行に1つずつ）")
    submitted = st.form_submit_button("表示する")

if submitted:
    st.subheader("📝 今日のスケジュール")
    for line in tasks.splitlines():
        if line.strip():
            st.write(f"✅ {line.strip()}")

