
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

- A working **user login and logout system**
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

## Person-by-Person Work Distribution

### **Mia**
- **Monday–Tuesday:** Set up `database.json`; tested JSON structure and verified player balance/wins/losses updates; created Use Case diagram; worked on the SRS. 
- **Wednesday:** Built `main.py` routes for login and dashboard; debugged login connection to `user.py`.  
- **Thursday:** Updated and finalized `README.md` with Grace; helped with debugging the main program; worked with Joelle to complete Use Case Diagram edits.


### **Ethan**
- **Monday–Tuesday:** Created `user.py` registration and login validation; integrated password verification; worked on SRS.  
- **Wednesday:** Built HTML and CSS templates for the login and dashboard pages via Flask; fixed login error handling and UI formatting issues; worked to debug the main program. 
- **Thursday:** Testing login persistence and debugging; handled code-cleanup details; finalized the logout registration on the  home page; finalized the HTML. 


### **Grace**
- **Monday–Tuesday:** Wrote `funds.py` (deposit logic) and logout functionality in `user.py`; created the file structure on Github; created the Class Diagram; worked on the SRS. 
- **Wednesday:** Integrating JSON and `user.py` into `funds.py`; finished README.md document in new branch; created portion of `player.py` in calling function to funds; corrected Taiga User Story structure and board; finalized SRS document from work done together in class.
- **Thursday:** Help with debugging main program; Finalize `README.md` final touches; worked with Joelle to complete Class Diagram edits. 


### **Joelle**
- **Monday–Tuesday:** Implemented `blackjack.py` core game logic (deck creation, card values, dealer AI); worked on the SRS. 
- **Wednesday:** Integrated blackjack backend into Flask routes (`main.py`); ran sample gameplay tests and debugged logic edge cases (demo recorded to Kevin); tested and debug the main page and program; created player class in `player.py`
- **Thursday:** Continue debugging program for home page; assist in reviewing UML Diagrams.


### **Day-by-Day Plan**
| Day | Goal | Deliverables |
|------|------|--------------|
| **Tuesday (by 10:30 PM)** | Backend setup | `database.json`, `blackjack.py`, `funds.py`, `user.py` complete; review UML diagrams |
| **Wednesday (by 8:00 PM)** | Frontend integration | `main.py` Flask routing and UI/UX templates ready |
| **Wednesday Evening** | Testing & Debugging | Sample run and bug fixes based on feedback |
| **Thursday (Class Time)** | Sprint Retrospective | Present and reflect on functionality and teamwork |
 **Friday (Online)** | Sprint Retrospective | Reflection on current sprint & improvement for next sprint |

### **What We Accomplished**
| Day | Goal | Deliverables |
|------|------|--------------|
| **Tuesday (by 10:30 PM)** | Backend setup | `database.json`, `blackjack.py`, `funds.py`, `user.py` complete; UML diagrams |
| **Wednesday (by 8:00 PM)** | Finish Backend setup | `blackjack.py`, `funds.py`, `user.py` updated |
| **Wednesday Evening** | Testing & Debugging | Sample run and bug fixes based on feedback, UI/UX created |
| **Thursday (Class Time)** | Cont. Testing & Debugging | Present and reflect on functionality and teamwork |
| **Friday (Online)** | Sprint Retrospective | Present and reflect on functionality and teamwork via Zoom |

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


4. Run the Flask app
**python app/main.py**

