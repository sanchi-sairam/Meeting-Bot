import streamlit as st
import pandas as pd
import requests
import io

API_URL = "http://localhost:8000/analyze/"

st.title("🤖 Meeting Bot (FastAPI + Transformers)")
st.markdown("Type a chat message to extract meeting info.")

if "meeting_data" not in st.session_state:
    st.session_state.meeting_data = []

message = st.text_input("💬 Enter a meeting message:")

if st.button("Submit"):
    if message:
        response = requests.post(API_URL, json={"text": message})
        if response.status_code == 200:
            data = response.json()
            st.session_state.meeting_data.append(data)
        else:
            st.error("API request failed. Is FastAPI server running?")

if st.session_state.meeting_data:
    df = pd.DataFrame(st.session_state.meeting_data)
    df = df.fillna('NA')
    st.subheader("📋 Extracted Info")
    st.dataframe(df)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    st.download_button(
        "Download as Excel",
        data=buffer.getvalue(),
        file_name="meeting_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
