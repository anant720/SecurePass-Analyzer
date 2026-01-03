# SecurePass Analyzer

A comprehensive, cybersecurity-focused web application for password strength analysis and breach detection. This project demonstrates secure coding practices, password analysis algorithms, and modern web development.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [How to Start](#how-to-start)
- [Project Structure](#project-structure)
- [File Explanations](#file-explanations)
- [Security Features](#security-features)
- [API Endpoints](#api-endpoints)
- [Scoring System](#scoring-system)
- [Future Enhancements](#future-enhancements)

## Features

### Password Strength Analysis
- Custom Rules Engine: Evaluates passwords based on length, character variety, patterns, and complexity
- zxcvbn Integration: Uses Dropbox's zxcvbn algorithm for realistic password strength estimation
- Combined Scoring: Merges custom rules and zxcvbn scores for comprehensive analysis
- Crack Time Estimation: Calculates estimated time to crack password using various attack methods

### Attack Simulation
- Dictionary Attack: Checks against common password lists
- Brute Force Estimation: Calculates possible combinations and estimated crack times for online attacks (rate-limited), offline fast attacks (GPU-based), and offline slow attacks (bcrypt hashing)

### Breach Detection
- Hashed Comparison: Uses SHA-256 hashing to check passwords against known breach databases
- Zero Storage: Passwords are never stored or logged
- Privacy-First: Only hash values are compared, ensuring complete privacy

### Security Features
- Rate Limiting: 5 requests per minute per IP address
- No Password Logging: Passwords are never logged or stored
- Hashed Comparison: All breach checks use cryptographic hashing
- CORS Enabled: Secure cross-origin resource sharing

## Architecture

```
┌─────────────┐
│   Frontend  │  HTML/CSS/JavaScript
│  (Browser)  │
└──────┬──────┘
       │ HTTP/REST API
       │
┌──────▼──────┐
│ Flask API   │  Rate Limiting, CORS
│  (Backend)  │
└──────┬──────┘
       │
   ┌───┴───┬──────────┬──────────────┐
   │       │          │              │
┌──▼──┐ ┌─▼───┐  ┌───▼───┐  ┌──────▼─────┐
│Rules│ │zxcvbn│  │Attack │  │   Breach   │
│Engine│ │      │  │Simulator│  │  Checker  │
└──────┘ └──────┘  └───────┘  └───────────┘
```

## Technology Stack

### Frontend
- HTML5: Semantic markup
- CSS3: Modern styling with Flexbox and animations (macOS-inspired glassmorphism design)
- JavaScript (Vanilla): No frameworks, pure ES6+

### Backend
- Python 3.8+: Core language
- Flask 3.0.0: Lightweight web framework
- Flask-CORS 4.0.0: Cross-origin resource sharing
- Flask-Limiter 3.5.0: Rate limiting middleware
- zxcvbn 4.4.28: Password strength estimation
- bcrypt 4.1.1: Password hashing (for demonstration)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Run the Backend Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Step 3: Open the Frontend

**Option A (Easiest):** Simply open `frontend/index.html` directly in your web browser

**Option B (Using a local server):** Open a new terminal window and run:

```bash
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Usage

1. Start the Backend: Run `python backend/app.py`
2. Open Frontend: Open `frontend/index.html` in your browser (or use local server)
3. Enter Password: Type a password in the input field
4. Analyze: Click "Analyze Password" or press Enter
5. Review Results: View strength analysis, breach status, and attack simulations

### Example Analysis

**Input**: `MyP@ssw0rd123!`

**Results**:
- Strength: Strong (75/100)
- Crack Time: ~2 years (offline slow hashing)
- Breach Status: Not found in breach database
- Dictionary Attack: Low vulnerability
- Brute Force: ~10^20 combinations

## How to Start

### Quick Start Commands

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend (Optional - only if using local server):**
```bash
cd frontend
python -m http.server 8000
```

Then open your browser and go to `http://localhost:8000` (if using server) or open `frontend/index.html` directly.

### Verification

- Backend is running if you see: `* Running on http://0.0.0.0:5000`
- Frontend is accessible at: `http://localhost:8000` (server) or via file:// (direct open)

### Troubleshooting

- **Port 5000 already in use**: Stop the process using port 5000 or change the port in `app.py`
- **Module not found errors**: Make sure you ran `pip install -r requirements.txt` in the backend directory
- **CORS errors**: The backend has CORS enabled by default, but make sure it's running on port 5000
- **Rate Limit Error**: The API limits to 5 requests per minute per IP. Wait 60 seconds and try again
- **Backend won't start**: Make sure Python 3.8+ is installed and all dependencies are installed
- **Frontend can't connect to API**: Verify the backend is running on `http://localhost:5000` and check browser console for errors

## Project Structure

```
password-analyzer/
│
├── backend/
│   ├── app.py                 # Flask API server
│   ├── strength_checker.py    # Main strength analyzer
│   ├── password_rules.py      # Custom rules engine
│   ├── attack_simulator.py    # Attack simulations
│   ├── breach_checker.py      # Breach detection
│   ├── password_generator.py  # Password generator
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html             # Main HTML
│   ├── style.css              # Styling (macOS-inspired)
│   └── script.js              # Frontend logic
│
└── README.md                  # This file
```

## File Explanations

### Backend Files

**`backend/app.py`**
- Main Flask application server and API endpoints
- Initializes Flask app with CORS and rate limiting
- Creates API endpoints for password analysis
- Handles HTTP requests and responses
- Implements security measures (rate limiting, no password logging)
- Coordinates between different analysis modules
- Endpoints: `/health`, `/api/analyze`, `/api/strength`, `/api/breach`, `/api/generate`

**`backend/strength_checker.py`**
- Main password strength analyzer combining custom rules and zxcvbn
- Integrates custom rules engine with zxcvbn algorithm
- Calculates combined strength score (0-100)
- Determines strength level (Very Weak to Very Strong)
- Estimates crack time in human-readable format
- Provides color coding for strength levels

**`backend/password_rules.py`**
- Custom rule-based password strength checking engine
- Implements custom password validation rules
- Scores passwords based on various criteria
- Identifies common patterns and weaknesses
- Provides detailed feedback and suggestions
- Rule checks: length, uppercase, lowercase, numbers, special chars, repeated chars, common patterns, sequential patterns

**`backend/attack_simulator.py`**
- Simulates common password attacks (dictionary and brute force)
- Dictionary attack: Checks against top 100 common passwords
- Brute force estimation: Calculates possible combinations and crack times
- Provides attack time estimates for different scenarios (online, offline fast, offline slow)
- Character set analysis

**`backend/breach_checker.py`**
- Checks if password appears in known data breaches
- Maintains a database of common breached passwords
- Uses SHA-256 hashing for secure comparison
- Never stores or compares plain text passwords
- Provides breach status and recommendations

**`backend/password_generator.py`**
- Generates secure, random passwords
- Supports customizable options (length, character types)
- Generates memorable passwords (word-based)
- Calculates password entropy
- Uses cryptographically secure random number generation

### Frontend Files

**`frontend/index.html`**
- Main HTML structure and UI layout
- Header, input section, button group, generator panel
- Results section with all analysis results displayed in cards
- Footer with security notes

**`frontend/style.css`**
- macOS-inspired styling with glassmorphism effects
- Glassmorphic cards with blur effects
- Smooth animations and transitions
- Color-coded strength indicators
- Responsive grid layouts
- Mobile-friendly design

**`frontend/script.js`**
- Frontend JavaScript logic and API communication
- Handles user interactions
- Communicates with backend API
- Updates UI based on analysis results
- Manages password generator
- Implements copy to clipboard functionality

## Security Features

### What We Do
✅ **Hash Passwords**: All breach checks use SHA-256 hashing  
✅ **Rate Limiting**: Prevents abuse (5 requests/minute)  
✅ **No Logging**: Passwords are never logged  
✅ **No Storage**: Passwords are never stored  
✅ **CORS Protection**: Controlled cross-origin access  

### What We Don't Do
❌ Never send passwords to external services  
❌ Never store passwords in plain text  
❌ Never log passwords in any form  
❌ Never transmit passwords over unencrypted connections (in production)  

### Production Recommendations
- Use HTTPS/TLS for all connections
- Implement proper authentication for API access
- Use environment variables for sensitive configuration
- Deploy behind a reverse proxy (nginx, Apache)
- Use a production WSGI server (gunicorn, uWSGI)
- Implement proper logging and monitoring
- Consider using Have I Been Pwned API with k-anonymity

## API Endpoints

### `POST /api/analyze`
Comprehensive password analysis endpoint.

**Request:**
```json
{
  "password": "YourPassword123!"
}
```

**Response:**
```json
{
  "strength": {
    "final_score": 75.5,
    "strength_level": "Strong",
    "strength_color": "#00cc00",
    "crack_time_human": "2 years",
    ...
  },
  "breach_check": {
    "breached": false,
    "severity": "None",
    ...
  },
  "dictionary_attack": {...},
  "brute_force": {...}
}
```

### `POST /api/strength`
Password strength analysis only.

### `POST /api/breach`
Breach check only.

### `POST /api/generate`
Generate a secure password with customizable options.

### `GET /health`
Health check endpoint.

## Scoring System

### Custom Rules (0-100 points)
- Length ≥ 16: +25 points
- Length ≥ 12: +20 points
- Length ≥ 8: +10 points
- Uppercase: +10 points
- Lowercase: +10 points
- Numbers: +10 points
- Special chars: +15 points
- Repeated chars (3+): -10 points
- Common patterns: -15 points
- Sequential patterns: -10 points

### zxcvbn Integration (0-4 scale, weighted to 0-80)
- Score 0: Very Weak
- Score 1: Weak
- Score 2: Medium
- Score 3: Strong
- Score 4: Very Strong

### Final Score Calculation
```
Final Score = (Custom Score + zxcvbn Score × 20) / 2
```

### Strength Levels
- 80-100: Very Strong
- 60-79: Strong
- 40-59: Medium
- 20-39: Weak
- 0-19: Very Weak

## Future Enhancements

- [ ] Integration with Have I Been Pwned API (k-anonymity)
- [ ] Password generation suggestions
- [ ] Historical analysis tracking (anonymized)
- [ ] Multi-language support
- [ ] Advanced pattern detection
- [ ] User account management
- [ ] API key authentication
- [ ] Docker containerization
- [ ] Unit and integration tests
- [ ] Performance optimization

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**⚠️ Important**: This tool is for educational and demonstration purposes. Always use strong, unique passwords and enable two-factor authentication where available.

**🔒 Security Note**: In production environments, ensure all connections use HTTPS/TLS encryption.
