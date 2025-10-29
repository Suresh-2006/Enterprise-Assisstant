import os
import re
import smtplib
import random
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from chatbot import ask_ai, filter_bad_words

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # change this to a random secret key

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# In-memory store for OTPs - for demo only
otp_store = {}

# Company Info
company_name = "TechCorp Pvt Ltd"
company_policies = {
    "Leave Policy": "Employees can take 12 casual leaves per year.",
    "Work From Home": "Allowed twice a week with manager approval.",
    "Dress Code": "Formal wear Monday to Thursday, casuals on Friday.",
    "IT Support": "Contact ITHelp@techcorp.com for any issues.",
    "Employee Benefits": "Health insurance, travel allowance, and yearly bonus.",
    "Office Timings": "9 AM to 6 PM, Monday to Friday.",
    "Grievance Redressal": "Report concerns to HR or use the anonymous feedback portal.",
    "Performance Review": "Conducted every 6 months with clear KPIs."
}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            message = f"Subject: Your OTP Code\n\nYour OTP code is {otp}"
            server.sendmail(EMAIL_SENDER, email, message)
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    return True

def extract_text(file):
    try:
        temp_path = os.path.join("uploads", secure_filename(file.filename))
        os.makedirs("uploads", exist_ok=True)
        file.save(temp_path)
        
        reader = PdfReader(temp_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        os.remove(temp_path)
        return text or "No readable text found in the document."
    except Exception as e:
        print("Error extracting PDF text:", e)
        return "Error reading document."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_otp", methods=["POST"])
def send_otp_route():
    email = request.form.get("email")
    if not email or "@" not in email:
        return jsonify({"status": "error", "message": "Invalid email"})
    if send_otp(email):
        session["email"] = email
        return jsonify({"status": "success", "message": "OTP sent"})
    else:
        return jsonify({"status": "error", "message": "Failed to send OTP"})

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    email = session.get("email")
    if not email:
        return jsonify({"status": "error", "message": "No email in session"})
    otp = request.form.get("otp")
    if otp_store.get(email) == otp:
        session["verified"] = True
        otp_store.pop(email, None)
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Invalid OTP"})

@app.route("/chat", methods=["POST"])
def chat():
    if not session.get("verified"):
        return jsonify({"response": "Please verify your email first."})

    user_msg = request.form.get("message", "").lower()
    uploaded_file = request.files.get("file")

    # Check if the message asks about company policies
    keywords = ["policy", "policies", "leave", "work from home", "timing", "benefit", "review"]
    if any(word in user_msg for word in keywords):
        response_text = f"Here are the main company policies for {company_name}:\n"
        for key, value in company_policies.items():
            response_text += f"- {key}: {value}\n"
        return jsonify({"response": response_text})

    context_text = ""
    if uploaded_file and uploaded_file.filename.endswith(".pdf"):
        context_text = extract_text(uploaded_file)

    final_prompt = f"{context_text}\n\nUser: {user_msg}" if context_text else user_msg
    final_prompt = filter_bad_words(final_prompt)

    try:
        bot_response = ask_ai(final_prompt)
        bot_response = filter_bad_words(bot_response)
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
