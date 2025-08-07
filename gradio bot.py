import json
from datetime import datetime

import gradio as gr

from models.get_model import get_model_instance

MODEL_ID = "ibm/granite-13b-instruct-v2"

model = get_model_instance(MODEL_ID)
# === History storage ===
conversation_history = []

# === Categories ===
CATEGORIES = [
    "Water Supply Issues",
    "Electricity Problems",
    "Road & Infrastructure",
    "Waste Management",
    "Drainage & Sewage",
    "Public Safety",
    "Transport & Traffic",
    "Health & Sanitation",
    "Pollution",
    "Unauthorized Construction & Encroachment",
]


def build_prompt(history):
    joined = "\n".join(
        [f"{'User' if h['role']=='user' else 'AI'}: {h['content']}" for h in history]
    )
    instruction = f"""
You are a smart government grievance support bot designed to help citizens from diverse linguistic backgrounds.

You must:
1. Politely respond to greetings (like "hi", "hello", "namaste", "hola", etc.) and guide the user by saying:
   - "Would you like to register a complaint? Please provide the required details."

2. Collect the following details from the citizen if not already provided:
   - Full name
   - Type of identification (e.g. Aadhar, SSN)
   - Identification number
   - Full address (with street, city, state, and postal code)
   - Clear and detailed description of the issue (so you can evaluate criticality)

3. Classify the issue into one of the following categories:
   {", ".join(CATEGORIES)}

4. Evaluate the criticality on a scale of 1 to 5 based on urgency and impact.

5. If you do not have enough information, ask the user again with specific questions.

6. Your responses should be friendly, inclusive, and, if needed, offer to continue in the user's preferred language (e.g. "Would you prefer to continue in Hindi, Tamil, Bengali, etc.?").

7. Once all details are collected, respond ONLY with a JSON object like:

{{
  "name": "...",
  "type_of_identification": "...",
  "identification_number": "...",
  "location": "...",
  "category": "...",
  "context": "...",
  "criticality": 3
}}

Now continue this interaction:
{joined}
AI:"""
    return instruction


def chat(user_input, chat_history):
    conversation_history.append({"role": "user", "content": user_input})

    prompt = build_prompt(conversation_history)

    response = model.generate_text(
        prompt=prompt,
        params={"decoding_method": "greedy", "max_new_tokens": 500},
        raw_response=False,
    )

    conversation_history.append({"role": "assistant", "content": response})

    # Check if the AI produced final JSON
    try:
        data = json.loads(response)
        # Save to file
        complaint_record = {"timestamp": datetime.now().isoformat(), **data}
        with open("complaints.json", "a") as f:
            f.write(json.dumps(complaint_record) + "\n")

        # Reset conversation for next person
        conversation_history.clear()

        return chat_history + [(user_input, response)], gr.update(interactive=False)

    except json.JSONDecodeError:
        return chat_history + [(user_input, response)], gr.update()


# Gradio chat UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧾 Civic Issue Reporter (powered by IBM watsonx)")
    chatbot = gr.Chatbot()
    user_msg = gr.Textbox(label="Enter your message")
    send_btn = gr.Button("Submit")

    send_btn.click(fn=chat, inputs=[user_msg, chatbot], outputs=[chatbot, user_msg])
    user_msg.submit(fn=chat, inputs=[user_msg, chatbot], outputs=[chatbot, user_msg])

demo.launch()
