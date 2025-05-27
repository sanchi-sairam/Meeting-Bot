Overview
The Meeting Bot is a web application that allows users to input chat-style messages (like in Slack, Teams, or WhatsApp), and automatically extract structured meeting-related information such as:

🗓 Date

🕒 Time

✅ Action Items

🧠 Decisions

The extracted insights are displayed in a table and can be downloaded as an Excel file.


1. Install Dependencies
pip install -r requirements.txt

2. Start the FastAPI Backend
cd backend
uvicorn main:app --reload
Fast API server will run on http://localhost:8000

3. Start the Streamlit Frontend
cd frontend
streamlit run app.py
Streamlit UI server will run on http://localhost:8501
