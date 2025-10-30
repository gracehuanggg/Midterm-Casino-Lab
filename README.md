
# CMP521 Python Casino App — Sprint 2 (Group A)

**Sprint Duration:** October 13–17, 2025  
**Team Members:** Grace Huang, Mia Guo, Joelle Yang, Ethan Huang  
**Project Owner:** Kevin Santos  
**Framework:** Flask (Python 3.10+)

---

## 1. Project Overview

The **Python Casino Web App** is a Flask-based browser application where users can create an account, log in, deposit funds, and play a functioning **Blackjack** and **Slot Machine** game. The goal of this sprint is to complete the **Minimum Viable Product (MVP)** that integrates authentication, data storage, UI, and basic game mechanics.  

The system:
- Stores user accounts and balances in a **JSON database**
- Allows for user **registration**, **login**, and **logout**
- Lets users **deposit funds** and view them on the **dashboard**
- Runs a **playable Blackjack game** that updates user balances dynamically
- Runs a **slot machine game** that updates to JSON file
- Provides a simple **Flask front-end** with **basic color styling** for improved readability

---

## 2. File Structure

<pre>'''Midterm-Casino-Lab/
│
├── app/ 
│ ├── main.py # Flask entry point; connects all modules and handles routes; handles deposits
│ ├── blackjack.py # Blackjack game backend logic and rules
│ ├── player.py #Handles Player class
│ ├── slot.py # Slot machine logic (generates symbol)
│ └── user.py # Manages user registration, login, and logout
│
├── data/
│ └── database.json # JSON file for user data and balances
│├── docs/
│ └── Use_Case_Diagram.png #Documents the use case of the program
│ └── Class_Diagram.png #Documents the attributes and methods for each class
│ └── SRS_Document.pdf #Purpose, Scope, General Constraints, User Stories, Acceptance Criteria
│
└── README.md # Documentation'''</pre>

---

## 3. Feature Overview

### User Registration & Login (`user.py`)
- Register new users
- Validate login credentials
- Allow logout and redirect to the login page
- Auto-login newly created accounts
- Include a preferred name field for personalized home page greetings

### Deposit Funds/Wallet (`main.py`)
- Enable users to add funds
- Update funds into JSON data
- Reflect the new balance on the dashboard
- Limit excessive deposits (no more than 1 billion dollars)
- Shows all money values with two decimal places (to the cent)

### Casino Dashboard (`home.html` / `main.py`)
- Display username and current balance (balance hidden on initial login for privacy)
- Displays the user’s preferred name
- Buttons to deposit funds or play Blackjack
- Logout option for session security
- Shows user statistics for total money won, total money lost, and net value
- Improved color styling and layout for clarity and user experience

### Blackjack Game (`blackjack.py` & `player.py`)
- Standard Blackjack logic (hit, stand, dealer rules)
- Track bets and game outcomes
- Adjust player balance automatically
- Persist balance changes to JSON with two decimals

### Player Class (`player.py`)
- Keeps track of player attributes

### Slot Machine (`slot.py`, `main.py`)
- Allows the user to place a custom bet before spinning
- Randomly determines three symbols for each spin
- Winning combinations pay out automatically (3-match high payout, 2-match low payout)
- Bets must be within the user's balance and at least $0.01, and less than a billion dollars
- Updates the user's wins/losses based on the results
- Saves progress and updates to theJSON file

---

## 4. Diagrams and Documentation

**docs/** includes:
- **Use Case Diagram:** Player actions 
- **Class Diagram:** Displays methods and attributes for the program’s classes
- **SRS Document:** Outlines project scope, constraints, and user stories

---

## 5. How to Run the App

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

