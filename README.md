# Enterprise Assistant

Enterprise Assistant is an AI-powered chatbot developed using Flask, Deep Learning, and Natural Language Processing (NLP). It is designed to assist employees of a large organization by answering queries related to HR policies, IT support, company events, and other organizational topics.
The system also supports document upload and processing — allowing users to extract, summarize, and query information directly from PDF documents such as policy manuals or reports.

---

## Key Features

* **Secure Login with Email OTP (2FA)**
  Ensures only verified users can access the chatbot interface using a 6-digit OTP sent via email.

* **AI Chatbot with Context Awareness**
  Uses deep learning and NLP to understand user queries and provide relevant responses using the organization’s data.

* **Document Upload and Processing**
  Allows users to upload PDF documents (like HR manuals or IT policies). The chatbot extracts and understands the content for context-based Q&A.

* **Bad Language Filtering**
  Automatically filters out inappropriate language using a predefined dictionary.

* **Scalable and Fast Response**
  Optimized for low-latency replies (within 5 seconds) and supports multiple parallel users.

* **Simple and Elegant UI**
  Features a minimal light theme interface for a clean and user-friendly experience.

---

## Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **AI Integration:** OpenRouter/OpenAI API
* **Document Processing:** PyPDF2 for PDF text extraction
* **Email Service:** smtplib (Gmail SMTP)
* **Environment Management:** python-dotenv

---

## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/enterprise-assistant.git
cd enterprise-assistant
```

### 2. Create a Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in your root directory and add:

```
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_email_password
OPENAI_API_KEY=your_openrouter_api_key
```

### 5. Add Company Information

Create a file named `company.txt` in the project folder and enter:

```
TechCorp Pvt Ltd
```

### 6. Run the Flask App

```
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

---

## How It Works

1. **User Authentication** – The user enters their email, receives an OTP, and verifies identity.
2. **Chat Interface** – Once verified, the chat interface is activated.
3. **Document Upload** – Users can upload company-related PDFs (e.g., HR or IT documents).
4. **Smart Query Response** – The AI assistant reads the uploaded file and responds contextually to the user’s questions.
5. **Secure Interaction** – All inputs are filtered for bad language, and the backend ensures data isolation per user session.

---

## Folder Structure

```
enterprise-assistant/
│
├── app.py                # Main Flask backend
├── chatbot.py            # AI and text filtering logic
├── company.txt           # Contains organization name
├── requirements.txt      # Required dependencies
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── style.css         # Styling for frontend
│   └── script.js         # Frontend logic (OTP & chat)
├── uploads/              # Temporary file uploads
└── README.md
```

---

## Example Use Cases

* Employees ask HR-related questions like leave policy, holidays, or working hours
* IT staff query troubleshooting steps for common technical issues
* Managers upload event documents and get instant summaries or keyword extractions
* General users ask about company rules, events, or contact points

---

## Future Enhancements

* Integration with real company HR and IT databases
* Support for additional document types (Word, Excel, text files)
* Multi-language support for regional accessibility
* Dashboard for chat analytics and employee feedback
* Persistent chat memory and personalized responses

---


## License

This project is developed for educational and hackathon purposes.
You are free to modify and extend it under the MIT License.

---
