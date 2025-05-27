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

3. Start the Streamlit Frontend
cd frontend
streamlit run app.py
==================================================================================================================================================================================================================
📊 System Overview
The Meeting Bot system is designed to extract structured insights like date, time, actions, and decisions from:

User-input chat messages

Uploaded meeting transcripts (PDF/TXT)

📌 Key Features
✅ Text and file input
✅ FastAPI-powered backend using open-source LLM
✅ Transformers model via Hugging Face
✅ Streamlit UI with export to Excel
✅ JSON-format extraction for accuracy

🗺️ System Flow Diagram
Here's the high-level system flow:

plaintext
Copy
Edit
+-----------------+         +--------------------+         +----------------------------+
|   User (Browser)|  --->   |  Streamlit Frontend|  --->   |   FastAPI Backend          |
|  - Input message|         |                    |         |  - Accepts /analyze/ API   |
|  - Upload file  |         |  - UI for input    |         |  - Accepts /analyze_file/  |
|                 |         |  - Shows results   |         |  - Calls Transformers      |
+-----------------+         +--------------------+         +----------------------------+
                                                                  |
                                                                  v
                                                      +------------------------+
                                                      | Hugging Face Model     |
                                                      | (e.g., LaMini-Flan-T5) |
                                                      +------------------------+
                                                                  |
                                                                  v
                                                      +------------------------+
                                                      | JSON Output with       |
                                                      | Date, Time, etc.       |
                                                      +------------------------+

🏗️ System Components
1. Frontend: Streamlit
Text input for single messages

File uploader for transcripts (.txt, .pdf)

Sends data to FastAPI using requests

Displays results in a table

Offers Excel download of extracted data

2. Backend: FastAPI
Endpoints:
POST /analyze/ → accepts a single message

POST /analyze_file/ → accepts .txt or .pdf uploads

Processing:
Uses Hugging Face pipeline("text2text-generation")

Uses an optimized prompt to extract:

Date

Time

Actions

Decisions

Model (customizable):
python
Copy
Edit
pipeline("text2text-generation", model="MBZUAI/LaMini-Flan-T5-783M")
🧠 Prompt Structure
For accuracy, few-shot prompting is used:

text
Copy
Edit
You are a helpful assistant...
Message: "Let's meet on Friday at 2 PM."
Output:
{"date": "Friday", "time": "2 PM"}
📁 Project Structure
bash
Copy
Edit
meeting-bot/
│
├── backend/
│   └── main.py         # FastAPI server logic
│
├── frontend/
│   └── app.py          # Streamlit app
│
├── requirements.txt    # All dependencies
└── README.md           # Documentation
🛠️ Installation & Usage
1. Install requirements
bash
Copy
Edit
pip install -r requirements.txt
pip install PyMuPDF
2. Start backend
bash
Copy
Edit
cd backend
uvicorn main:app --reload
3. Start frontend
bash
Copy
Edit
cd frontend
streamlit run app.py
📦 Output Format
Message	Date	Time	Actions	Decisions
"Meeting on June 1 at 3PM..."	June 1	3 PM	John to send update	Use option A for rollout

Can be exported to Excel.

🧩 Future Improvements
 Add support for .docx

 Normalize “next Monday” to real date (dateparser)

 Deploy to Streamlit Cloud + Hugging Face Spaces

 Add entity extraction (people, projects)
