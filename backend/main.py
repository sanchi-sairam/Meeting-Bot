from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

app = FastAPI()

# Load the language model
model = pipeline("text2text-generation", model="google/flan-t5-base")

# model = pipeline("text2text-generation", model="MBZUAI/LaMini-Flan-T5-783M")


class Message(BaseModel):
    text: str

@app.post("/analyze/")
def analyze_message(msg: Message):
    prompt = f"""
        You are a helpful assistant that extracts scheduling information from messages.

        Your task is to read the following message and identify:
        - The date of the meeting (if any)
        - The time of the meeting (if any)

        Please follow these instructions:
        1. Return the result in JSON format with two fields: "date" and "time".
        2. If the message does not contain a date or time, use null for that field.
        3. Only return the JSON. Do not include any explanations or extra text.

        ### Example 1:
        Message: "Let's meet on June 15th at 10:30 AM."
        Output:
        {{"date": "June 15th", "time": "10:30 AM"}}

        ### Example 2:
        Message: "Team sync next Monday at 3 PM."
        Output:
        {{"date": "next Monday", "time": "3 PM"}}

        ### Example 3:
        Message: "Please check the file I sent yesterday."
        Output:
        {{"date": null, "time": null}}

        ### Now analyze this message:
        Message: "{msg.text}"
        Output:
    """
    response = model(prompt)[0]["generated_text"]

    result = {
        "Message": msg.text,
        "Date": "",
        "Time": "",
        "Actions": "",
        "Decisions": ""
    }

    print(response)
    for line in response.strip().split("\n"):
        if line.lower().startswith("date"):
            result["Date"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("time"):
            result["Time"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("actions"):
            result["Actions"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("decisions"):
            result["Decisions"] = line.split(":", 1)[-1].strip()

    print(result)
    return result

# Run locally
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
