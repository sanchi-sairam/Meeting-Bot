from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
import json

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

        Please follow these instructions:
        1. Return the result in JSON format with fields: "date", "time", "action_plan", "decision".
        2. If the message does not contain a date or time, use null for that field.
        3. Only return the JSON. Do not include any explanations or extra text.

        ### Example 1:
        Message: "Let's meet on June 15th at 11:30 AM."
        Output:
        {{"date": "June 15th", "time": "11:30 AM", "action_plan": null, "decision": null}}

        ### Example 2:
        Message: "Team sync Tuesday at 2:00 PM."
        Output:
        {{"date": "next Tuesday", "time": "2 PM", "action_plan": null, "decision": null}}

        ### Example 3:
        Message: "Please check the file I sent yesterday."
        Output:
        {{"date": null, "time": null,"action_plan": null, "decision": null}}

        ###Example 4:
        Message: "Let's meet on June 15th at 10:45 AM. We'll finalize the budget proposal during the meeting."
        Output:
        {{"date": "June 15th", "time": "10:45 AM", "action_plan": "finalize the budget proposal", "decision": null}}

        ###Example 5:
        Message: "Team sync next Monday at 3 PM. Decision: Move forward with Option B."
        Output:
        {{"date": "next Monday", "time": "3 PM", "action_plan": null, "decision": "Move forward with Option B"}}

        ###Example 6:
        Message: "Let's meet on Friday at 12:20 PM for discussing about the application development plan."
        Output:
        {{"date": "Monday", "time": "12:20 PM", "action_plan": "To discuss development plan", "decision": "Application development"}}


        ### Now analyze this message:
        Message: "{msg.text}"
        Output:
    """
    response = model(prompt)[0]["generated_text"]
    print(response)
    response_dict = {}
    for i in response.split(","):
        key, value = i.split(":")[0], i.split(":")[-1]
        response_dict[key.strip('\'" ')] = value.strip('\'" ')
    
    print(response_dict)
    result = {
        "Message": msg.text,
        "Date": response_dict["date"],
        "Time": response_dict["time"],
        "Actions": response_dict["action_plan"],
        "Decisions": response_dict["decision"] if "decision" in response_dict.keys() else None,
        "Meeting link" : None
    }

    # for line in response.strip().split("\n"):
    #     if line.lower().startswith("date"):
    #         result["Date"] = line.split(":", 1)[-1].strip()
    #     elif line.lower().startswith("time"):
    #         result["Time"] = line.split(":", 1)[-1].strip()
    #     elif line.lower().startswith("actions"):
    #         result["Actions"] = line.split(":", 1)[-1].strip()
    #     elif line.lower().startswith("decisions"):
    #         result["Decisions"] = line.split(":", 1)[-1].strip()

    print(result)
    return result

# Run locally
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
