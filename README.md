# CMP521 Python Casino App — Sprint 1 (Group A)

**Sprint Duration:** October 13–17, 2025  
**Team Members:** Grace Huang, Mia Guo, Joelle Yang, Ethan Huang  
**Project Owner:** Kevin Santos  
**Framework:** Flask (Python 3.10+)

---

## 1. Project Overview

The **Python Casino Web App** is a Flask-based browser application where users can create an account, log in, deposit funds, and play a functioning **Blackjack** game. The goal of this sprint is to complete the **Minimum Viable Product (MVP)** that integrates authentication, data storage, UI, and basic game mechanics.  

The system:
- Stores user accounts and balances in a **JSON database**
- Allows for user **registration**, **login**, and **logout**
- Lets users **deposit funds** and view them on the **dashboard**
- Runs a **playable Blackjack game** that updates user balances dynamically
- Provides a simple **Flask front-end**

---

## 2. Sprint 1 Goal

The goal of this sprint is to complete the **Minimum Viable Product (MVP)** for the **Python Casino** web app.  
The MVP must include:

- A working **user login and logout system***
- A **casino dashboard** that displays username and user balance
- A **deposit funds** feature connected to the JSON database
- A playable **Blackjack game**
- All functionality integrated into a **Flask web app**

---

## 3. File Structure

<pre>'''Midterm-Casino-Lab/
│
├── app/ 
│ ├── main.py # Flask entry point; connects all modules and handles routes
│ ├── blackjack.py # Blackjack game backend logic and rules
│ ├── player.py #Handles player class
│ ├── funds.py # Handles deposit and balance management
│ └── user.py # Manages user registration, login, and logout
│
├── data/
│ └── database.json # JSON file for user data and balances
│├── docs/
│ └── Use_Case_Diagram.png #Documents the use case of the program
│ └── Class_Diagram.png #Documents the attributes and methods for each class
│ └── SRS_Document.pdf #Purpose, Scope, General Constriants, User Stories, Acceptance Criteria
│
└── README.md # Documentation'''</pre>

---

## 4. Task Assignment & Story Points (Total: 17 SP)

**Sprint Goal:** Build the MVP Flask app with login/logout, dashboard display, deposit funds, and a Blackjack game.

| File / Feature | Description | Assigned To | Story Points |
|-----------------|--------------|--------------|---------------|
| `data/database.json` | JSON format for data storage | Mia | 1 |
| `blackjack.py` | Blackjack logic and game functions | Joelle | 3 |
| `player.py` | Player attributes and methods | Grace (Funds component), Joelle (Player class) | 2 |
| `funds.py` | Handles user deposits and balance updates | Grace | 2 |
| `user.py` | Login, registration, and logout processes | Ethan (Login & Registration), Grace (Logout) | 3 |
| `main.py` | Connects routes and runs the Flask web app | Mia (Login route), Joelle (Home routes) | 3 |
| `templates` & `static` | Frontend layout and styling (HTML/CSS) | Ethan | 2 |
| `README.md` | Project documentation and setup guide | Mia & Grace | 1 |

**Total = 17 SP**

---

## 5. Project Timeline

### **Day-by-Day Plan**
| Day | Goal | Deliverables |
|------|------|--------------|
| **Tuesday (by 10:30 PM)** | Backend setup | `database.json`, `blackjack.py`, `funds.py`, `user.py` complete; review UML diagrams |
| **Wednesday (by 8:00 PM)** | Frontend integration | `main.py` Flask routing and UI/UX templates ready |
| **Wednesday Evening** | Testing & Debugging | Sample run and bug fixes based on feedback |
| **Thursday (Class Time)** | Sprint Retrospective | Present and reflect on functionality and teamwork |

### **What We Accomplished**
| Day | Goal | Deliverables |
|------|------|--------------|
| **Tuesday (by 10:30 PM)** | Backend setup | `database.json`, `blackjack.py`, `funds.py`, `user.py` complete; UML diagrams |
| **Wednesday (by 8:00 PM)** | Finish Backend setup | `blackjack.py`, `funds.py`, `user.py` updated |
| **Wednesday Evening** | Testing & Debugging | Sample run and bug fixes based on feedback, UI/UX created |
| **Thursday (Class Time)** | Cont. Testing & Debugging | Present and reflect on functionality and teamwork |
| **Friday (Online)** | Sprint Retrospective | Present and reflect on functionality and teamwork via Zoom |

### **Developer Notes**
- Ethan and Joelle finish their assigned tasks before Wednesday’s sample run.  
- Mia and Grace finalize files and verify functionality before class on Wednesday.  
- Debug and document all changes on Wednesday evening.

---

## 6. Feature Overview

### User Registration & Login (`user.py`)
- Register new users
- Validate login credentials
- Allow logout and redirect to login page

### Deposit Funds (`funds.py`)
- Enable users to add funds
- Update funds into JSON data
- Reflect new balance on dashboard

### Casino Dashboard (`home.html` / `main.py`)
- Display username and current balance
- Buttons to deposit funds or play Blackjack
- Logout option for session security

### Blackjack Game (`blackjack.py` & `player.py`)
- Standard Blackjack logic (hit, stand, dealer rules)
- Track bets and game outcomes
- Adjust player balance automatically
- Persist balance changes to JSON

### Player Class (`player.py`)
- Keeps track of player attributes

---

## 7. Diagrams and Documentation

**docs/** includes:
- **Use Case Diagram:** Player actions
- **Class Diagram:** Displays methods and attributes for program’s classes
- **SRS Document:** Outlines project scope, constraints, and user stories

---

## 8. How to Run the App

### Prerequisites
- Python 3.10 or later  
- Flask (`pip install flask`)  
- A text editor (VS Code recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/Midterm-Casino-Lab.git
   cd Midterm-Casino-Lab
2. **Create a virtual environment (recommended)***
python -m venv venv

Activate the environment:
macOS/Linux use
**source venv/bin/activate**
Windows (PowerShell) use
**venv\Scripts\activate**

3. **Install flask:**
pip install flask


5. Run the Flask app
python app/main.py

6. Open the app in your browser
Visit:
put HTML
