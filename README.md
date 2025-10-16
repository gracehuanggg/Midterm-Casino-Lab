## Midterm-Casino-Lab# CMP521 Python Casino App — Sprint 1 (Group A)

**Sprint Duration:** October 13–17, 2025  
**Team Members:** Grace Huang, Mia Guo, Joelle Yang, Ethan Huang
**Project Owner:** Kevin Santos
**Framework:** Flask and Python

---

## Sprint 1 Goal

The goal of this sprint is to complete the **Minimum Viable Product (MVP)** for the **Python Casino** web app.  
The MVP must include:

- A working “user login and logout system”
- A “casino dashboard” that displays username and user balance
- A “deposit funds” feature connected to the JSON database
- A playable “Blackjack game”
- All functionality integrated into a “Flask web app”

---

##  File Structure

---
<pre>
Midterm-Casino-Lab/
│
├── main.py # Flask entry point; connects all modules and handles routes 
│
├── blackjack.py # Blackjack game backend logic and rules
├── funds.py # Handles deposit and balance management 
├── user.py # Manages user registration, login, and logout 
│
├── data/
│ └── database.json # JSON database storing user credentials and balances
│
├── templates/ # Flask HTML templates
│ ├── login.html # Login and registration page 
│ ├── home.html # Casino dashboard (welcome, add funds, blackjack, logout) 
│ └── blackjack.html # Blackjack game interface
│
├── static/ # Static assets for styling 
│ ├── style.css # Core CSS for UI layout and visuals
│ └── images/ # Optional image folder for future UI assets
│
├── docs/
│ └── UML_Diagram.png # Combined UML Case and Class Diagram 
│
├── README.md # Project documentation 
</pre>

---

##   Feature Overview  

### User Registration & Login (user.py)
- Create new user accounts with usernames  
- Store and validate credentials in `users.json`  
- Assign default starting balance ($500)  
- Manage user sessions with Flask  

### Deposit Funds (funds.py)
- Allow logged-in users to add funds to their balance  
- Validate deposit amount and update JSON data  

### Casino Dashboard (home.html / main.py)
- Display logged-in username and current balance  
- Include navigation to Deposit and Blackjack pages  

### Blackjack Game (blackjack.py)
- Playable game versus automated dealer  
- Follows standard Blackjack rules  
- Bets update the player’s balance (win, loss, tie)  
- Results persist to JSON database  

---

## 5. How to Run the App  
