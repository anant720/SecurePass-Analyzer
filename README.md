# 🔐 SecurePass Analyzer

**A Cybersecurity-Focused Password Strength & Breach Analysis Tool**

SecurePass Analyzer is a **full-stack cybersecurity web application** that analyzes password strength, simulates real-world attacks, and checks for data breach exposure — **without ever storing or logging passwords**.

This project demonstrates **secure coding practices**, **password security concepts**, and **backend–frontend integration**, making it ideal for **placements, internships, and cybersecurity roles**.

---

## 🚀 Why This Project Matters (For Recruiters)

✔ Implements **real-world password attack models**
✔ Follows **privacy-first & zero-storage security principles**
✔ Uses **industry-recognized algorithms (zxcvbn, bcrypt)**
✔ Clean **API-based architecture**
✔ Strong example of **secure backend design in Python (Flask)**

> 🔍 This project reflects how modern security tools are built — not just theory, but practice.

---

## 📌 Key Features

### 🔑 Password Strength Analysis

* **Custom Rules Engine**
  Evaluates:

  * Length
  * Uppercase / lowercase
  * Numbers & special characters
  * Repeated and sequential patterns
* **zxcvbn Integration (by Dropbox)**
  Provides realistic strength estimation based on real-world password data
* **Final Strength Score (0–100)**
  Combines custom rules + zxcvbn for accurate results
* **Crack Time Estimation**
  Displays human-readable crack times (seconds → years)

---

### 🧨 Attack Simulation (Educational)

* **Dictionary Attack Check**
  Tests against commonly used passwords
* **Brute Force Estimation**

  * Online attack (rate-limited)
  * Offline fast attack (GPU)
  * Offline slow attack (bcrypt)

> ⚠️ No real attacks are performed — only **mathematical simulations**.

---

### 🕵️ Breach Detection (Privacy-First)

* Passwords are **never stored**
* Passwords are **never logged**
* Uses **SHA-256 hashing** for breach comparison
* Only hashes are checked — **zero plaintext exposure**

---

## 🛡️ Built-in Security Measures

* ✅ Rate Limiting: **5 requests/min per IP**
* ✅ CORS Protection enabled
* ✅ Zero password storage
* ✅ No third-party password sharing
* ✅ Backend-only processing

---

## 🧠 System Architecture

```
Frontend (HTML/CSS/JS)
        ↓
REST API (Flask)
        ↓
────────────────────────────
| Strength Analyzer (Rules) |
| zxcvbn Engine             |
| Attack Simulator          |
| Breach Checker            |
────────────────────────────
```

---

## 🧰 Technology Stack

### Frontend

* **HTML5** – Semantic structure
* **CSS3** – Glassmorphism UI (macOS-style)
* **Vanilla JavaScript (ES6+)** – No frameworks

### Backend

* **Python 3.8+**
* **Flask 3**
* **Flask-CORS**
* **Flask-Limiter**
* **zxcvbn**
* **bcrypt**

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.8+
* pip
* Any modern web browser

---

### Step 1: Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

📍 Backend runs on: `http://localhost:5000`

---

### Step 2: Frontend Setup

**Option 1 (Simple):**
Open `frontend/index.html` directly in your browser

**Option 2 (Recommended):**

```bash
cd frontend
python -m http.server 8000
```

📍 Open: `http://localhost:8000`

---

## 🧪 How to Use

1. Start backend server
2. Open frontend
3. Enter a password
4. Click **Analyze Password**
5. View:

   * Strength score
   * Crack time
   * Breach status
   * Attack vulnerability

---

### 🔍 Example Output

**Password:** `MyP@ssw0rd123!`

* Strength: **Strong (75/100)**
* Estimated crack time: **~2 years**
* Breach status: **Safe**
* Dictionary attack risk: **Low**

---

## 📁 Project Structure

```
SecurePass-Analyzer/
│
├── backend/
│   ├── app.py
│   ├── strength_checker.py
│   ├── password_rules.py
│   ├── attack_simulator.py
│   ├── breach_checker.py
│   ├── password_generator.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## 🔎 Backend Module Overview

| File                    | Purpose                            |
| ----------------------- | ---------------------------------- |
| `app.py`                | API server, rate limiting, routing |
| `strength_checker.py`   | Final strength scoring logic       |
| `password_rules.py`     | Custom rule engine                 |
| `attack_simulator.py`   | Attack time estimation             |
| `breach_checker.py`     | Secure breach detection            |
| `password_generator.py` | Secure password creation           |

---

## 🌐 API Endpoints

| Endpoint        | Method | Description        |
| --------------- | ------ | ------------------ |
| `/api/analyze`  | POST   | Full analysis      |
| `/api/strength` | POST   | Strength only      |
| `/api/breach`   | POST   | Breach check       |
| `/api/generate` | POST   | Password generator |
| `/health`       | GET    | Server health      |

---

## 📊 Scoring Logic (Simplified)

```
Final Score =
(Custom Rules Score + (zxcvbn Score × 20)) / 2
```

### Strength Levels

* **80–100** → Very Strong
* **60–79** → Strong
* **40–59** → Medium
* **20–39** → Weak
* **0–19** → Very Weak

---

## 🔮 Future Enhancements

* 🔗 Have I Been Pwned API (k-anonymity)
* 🔐 API authentication
* 🐳 Docker deployment
* 🧪 Unit & integration testing
* 🌍 Multi-language support
* 📈 Performance optimization

---

## 📜 License

Open-source — **for educational & learning purposes**

---

## 🤝 Contributions

Pull requests are welcome.
Feel free to fork and enhance!

---

## ⚠️ Disclaimer

This project is built for **learning and demonstration**.
Always use **unique passwords** and **enable 2FA** in real syste
