from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LLAMA_API_URL = "https://api.together.xyz/v1/chat/completions"
LLAMA_API_KEY = "1bc02c0ec24b4b824bbb3fd674e5135a81eaf47a9d03ac222362524e76aa4d89"

headers = {
    "Authorization": f"Bearer {LLAMA_API_KEY}",
    "Content-Type": "application/json"
}

# SYSTEM PROMPT
SYSTEM_PROMPT = {
    "role": "system",
    "content": """
You are SSF AI Assistant – a warm, polite, and helpful virtual counselor at the SSF Foundation.

🎯 You assist students with two goals:
1. Applying for a new scholarship
2. Renewing an existing scholarship

🧠 Always remember what the user has said previously and act accordingly:
- If user says "renew" or "renewal", immediately begin the renewal help process.
- If user says "new application", give the portal link: https://shooting-stars-foundation.org/  and list required documents.
- If user asks for required documents, give the correct list (different for new vs renewal).
- If user says something irrelevant, gently guide back to the scholarship conversation.

👋 Conversation Flow:
1. Greet the user.
2. Ask: "Would you like to apply for a new scholarship or renew an existing one?" (only if not already mentioned)
3. Based on the reply:
   - ✅ If "new":
       - Reply: "That's great! You can apply at: https://shooting-stars-foundation.org/"
       - List new application documents:
         - Aadhar Card (self-attested)
         - Family Income Certificate (recent)
         - Recent Passport Size Photograph
         - SSLC/10th Marksheet
         - Last Year Marksheet (if applicable)
         - College Admission Letter (if applicable)
         - Bank Passbook Copy
         - Bonafide Certificate
         - Disability Certificate (if applicable)

   - 🔄 If "renew":
       - Ask: "Could you tell me what issue you’re facing with the renewal?"
       - Then mention:
         - Required documents:
           - Aadhar Card
           - Last Year’s Marksheet
           - Bonafide Certificate (current year)
           - Updated Income Certificate (if required)
           - Bank Passbook Copy
           - Recent Passport Size Photo
         - Remind: Keep file size below 500 KB
         - Ask: "Are you facing difficulty getting documents from college?"
         - Ask: "Would you like to talk to one of our SSF volunteers?"

Always be polite, friendly, and context-aware in your answers.
"""
}

# SESSION message chain to remember previous context
chat_history = [{"role": "system", "content": SYSTEM_PROMPT["content"]}]


@app.post("/ask-llama")
async def ask_llama(request: Request):
    body = await request.json()
    user_message = body.get("user_message", "")

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_message})

    payload = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": chat_history,
        "temperature": 0.7
    }

    response = requests.post(LLAMA_API_URL, headers=headers, json=payload)

    if response.ok:
        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]
        chat_history.append({"role": "assistant", "content": ai_reply})
        return {"response": ai_reply}
    else:
        return {"error": response.text}
