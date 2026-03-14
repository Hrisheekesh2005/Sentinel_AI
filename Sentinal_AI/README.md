# 🛡 Sentinal AI  
### Agentic Digital Safety Shield for Scam Detection

SurakshaLens AI is an intelligent scam detection web platform designed to identify fraudulent SMS and WhatsApp messages in real time. It combines Machine Learning and rule-based reasoning to detect scams, generate risk scores, and provide proactive safety actions.

---

## 🚀 Live Deployment

- 🌐 Frontend (Vercel) – Static Web Interface  
- ⚙ Backend (Render) – FastAPI + ML Model  

---

## 🧠 How It Works

SurakshaLens AI follows a hybrid detection architecture:

### 1️⃣ Machine Learning Layer
- Logistic Regression classifier  
- Trained on labeled scam dataset (`text`, `label`)
- Uses TF-IDF vectorization
- Predicts scam probability  

### 2️⃣ Rule-Based Risk Engine
- Detects urgency phrases (e.g., "urgent", "immediately")
- Flags OTP / PIN / CVV requests
- Identifies financial impersonation patterns
- Extracts suspicious URLs  

### 3️⃣ Risk Scoring System
Combines ML confidence + rule triggers to produce:
- **SAFE**
- **SUSPICIOUS**
- **SCAM**

With a transparent reasoning list explaining the decision.

---

## ✨ Key Features

- 🔍 Real-time message analysis  
- 📊 Dynamic risk score  
- 🧾 Explainable AI reasoning  
- 📱 Phone number extraction  
- 💳 UPI ID detection  
- 🔗 Suspicious link detection  
- 📄 Auto-generate cybercrime complaint PDF  
- 📧 One-click complaint email drafting  
- 🟢 WhatsApp alert sharing  

---

## 🏗 Tech Stack

### Frontend
- HTML  
- TailwindCSS  
- JavaScript  
- jsPDF  
- Hosted on Vercel  

### Backend
- FastAPI  
- Scikit-learn  
- Pandas  
- Joblib  
- Uvicorn  
- Hosted on Render  

---

## 📁 Project Structure
SurakshaLensAI/
│
├── backend/
│ ├── main.py
│ ├── agent.py
│ ├── rules.py
│ ├── train.py
│ ├── model.pkl
│ ├── vectorizer.pkl
│ ├── scam_data.csv
│ └── requirements.txt
│
├── frontend/
│ └── index.html
│
├── README.md
└── .gitignore


---

## ⚙️ Local Setup

### 1️⃣ Clone Repository
git clone https://github.com/your-username/SurakshaLensAI.git
cd SurakshaLensAI/backend


### 2️⃣ Install Dependencies
pip install -r requirements.txt


### 3️⃣ Run Backend
uvicorn main:app --reload


Backend runs at: http://127.0.0.1:8000/


### 4️⃣ Open Frontend

Open `frontend/index.html` in your browser.

---

## 🌐 Deployment Guide

### Backend (Render)

Build Command: pip install -r requirements.txt


Start Command: uvicorn main:app --host 0.0.0.0 --port 10000


### Frontend (Vercel)

- Import GitHub repository
- Set root directory to `frontend`
- Deploy

Update API URL inside `index.html`:


---

## 🎯 Project Objective

Digital fraud is rapidly increasing, especially OTP and banking impersonation scams.  
SurakshaLens AI demonstrates how explainable AI + practical UI design can create a proactive digital safety assistant rather than just a passive classifier.

---

## 📌 Future Improvements

- Deep learning NLP model (BERT)
- URL reputation API integration
- Real-time phishing link scanning
- SMS integration
- Browser extension version

---

## Team

**Jaisy Sunil**  

**Aardra SV**

**Hrisheekesh Narayan P E**

**Mohammed Ameen**

B.Tech Electronics & Communication Engineering  
CUSAT  

---

## 🛡 Final Statement

SurakshaLens AI is not just a classifier —  
it is an intelligent agent designed to actively protect users in the digital space.
