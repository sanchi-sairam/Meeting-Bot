import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000/analyze/"

st.title("🤖 Meeting Bot (FastAPI + Transformers)")
st.markdown("Type a chat message to extract meeting info.")

if "meeting_data" not in st.session_state:
    st.session_state.meeting_data = []

message = st.text_input("💬 Enter a meeting message:")

if st.button("Analyze"):
    if message:
        response = requests.post(API_URL, json={"text": message})
        if response.status_code == 200:
            data = response.json()
            st.session_state.meeting_data.append(data)
        else:
            st.error("API request failed. Is FastAPI server running?")

if st.session_state.meeting_data:
    df = pd.DataFrame(st.session_state.meeting_data)
    st.subheader("📋 Extracted Info")
    st.dataframe(df)

    st.download_button(
        "📥 Download as Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="../utils/meeting_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
