import streamlit as st

st.title("フォーム機能 基本コード例")
st.caption("st.form の基本的な使い方")

st.markdown("---")

# st.form 例
st.markdown("**st.form 例:**")
with st.form("user_form_basic"):
   st.write("ユーザー情報を入力してください (フォーム例)")
   name = st.text_input("名前", key="form_name_basic") # Add key
   age = st.number_input("年齢", min_value=0, max_value=120, key="form_age_basic") # Add key

   # フォーム送信ボタン
   submitted = st.form_submit_button("登録", key="form_submit_basic") # Add key

   if submitted:
       st.write(f"名前: {name}, 年齢: {age} で登録しました。")

st.markdown("---")
st.info("これはフォーム機能の基本コード例です。") 
