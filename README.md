# Smart ATM System

A complete smart ATM prototype integrating embedded systems, backend development, database systems, IoT communication, and mechanical design into a real-world banking simulation platform.

This project combines custom hardware, a web-based banking system, real-time database communication, and a CNC-manufactured ATM enclosure to simulate modern ATM operations.

---

# Project Overview

The Smart ATM System was developed to simulate the functionality of a real banking ATM while combining multiple engineering domains into a single integrated solution.

The system supports:
- RFID-based authentication
- PIN verification
- Banking transaction simulation
- Real-time hardware-database communication
- Interactive ATM user interface
- Embedded hardware control
- Custom PCB integration
- CNC-manufactured ATM enclosure

This project represents the integration of software engineering, embedded systems, IoT, database management, and mechanical design.

---

# Features

## Authentication System
- RFID card authentication
- PIN verification system
- Secure user validation

## Banking Operations
- Balance inquiry
- Deposit simulation
- Withdrawal simulation
- Transaction processing

## Real-Time Communication
- Hardware-to-backend communication
- Real-time database synchronization
- Serial communication integration

## Interactive ATM Interface
- Keypad interaction
- LED indicators
- Buzzer feedback
- ATM display interface

---

# Hardware Design

The ATM hardware was designed using a custom embedded architecture based on:

- ESP32
- RFID module
- Keypad matrix
- LEDs
- Buzzer
- Serial communication modules

The hardware system communicates directly with the backend server and banking database to perform authentication and transaction operations.

---

# Mechanical Design

The ATM enclosure was fully designed using SOLIDWORKS and prepared for CNC manufacturing.

## Mechanical Features
- Custom ATM frame
- CNC-compatible panel design
- Interlocking assembly structure
- Compact electronics placement
- Wiring management support
- Prototype-ready structure

## Manufacturing
- CNC cutting compatible
- Laser cutting compatible
- Modular assembly design

---

# Software Architecture

The backend system was developed using:

- Python
- Flask
- Microsoft SQL Server

## Backend Responsibilities
- User authentication
- Account verification
- Balance management
- Transaction handling
- ATM-hardware communication
- Database operations

---

# Technologies Used

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Database | Microsoft SQL Server |
| Frontend | HTML, CSS, JavaScript |
| Embedded Systems | ESP32 |
| Communication | Serial Communication |
| Authentication | RFID |
| CAD Design | SOLIDWORKS |
| Manufacturing | CNC Cutting |

---

# System Architecture

```text
User
 ↓
ATM Interface
(HTML/CSS/JS)
 ↓
Flask Backend
(main.py)
 ↓                ↓
Database         Hardware
(db.py)      (ESP32 + RFID)
 ↓
Microsoft SQL Server
```

---

# Project Structure

```bash
Atm-Machine-System/
│
├── backend/
│   ├── main.py
│   ├── db.py
│   └── serial_reader.py
│
├── frontend/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── app.js
│       ├── style.css
│       └── assets/
│
├── hardware/
│   ├── esp32/
│   ├── pcb_design/
│   ├── wiring/
│   └── firmware/
│
├── mechanical_design/
│   ├── solidworks/
│   ├── cnc_files/
│   └── renders/
│
├── database/
│   ├── backup/
│   ├── sql_scripts/
│   └── erd/
│
├── screenshots/
│
├── docs/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Database System

The database system manages:
- User accounts
- Customer information
- RFID authentication data
- PIN verification
- Transaction records
- Account balances

The system uses Microsoft SQL Server for secure banking data management.

---

# How the System Works

## Authentication Flow

1. User scans RFID card
2. ESP32 sends card data to backend
3. Backend verifies user from database
4. User enters PIN
5. PIN is validated
6. ATM operations become available

---

## Transaction Flow

1. User selects transaction
2. Request is sent to Flask backend
3. Database operation is executed
4. Balance is updated
5. Result is returned to ATM interface
6. Hardware indicators provide feedback

---

# Future Vision

One of the most exciting aspects of the project is its future scalability.

Currently, deposits and withdrawals are virtual simulations, but future versions aim to transform the ATM into a more realistic smart banking machine.

## Planned Features
- Real cash deposit and withdrawal simulation
- Custom 3D-printed coins
- Computer vision using ESP32-CAM
- Coin recognition and validation
- Automated counting system
- Enhanced ATM security
- Smart analytics dashboard
- Mobile banking integration
- Cloud database support
- Face recognition authentication
- Fingerprint authentication

---

# Engineering Domains Involved

This project combines multiple engineering disciplines:

| Domain | Implementation |
|---|---|
| Software Engineering | Flask backend & web interface |
| Database Systems | SQL Server database |
| Embedded Systems | ESP32 & RFID integration |
| IoT Systems | Hardware-software communication |
| Mechanical Design | SOLIDWORKS ATM enclosure |
| Manufacturing | CNC-cut structure |
| Electronics | Custom PCB design |

---

# Educational Value

This project provided practical hands-on experience in:
- Database systems
- Embedded systems
- Backend development
- IoT integration
- Hardware-software communication
- CNC manufacturing
- Mechanical design
- Real-time system integration

---

# Installation & Setup

## Clone Repository

```bash
git clone https://github.com/yourusername/Atm-Machine-System.git
cd Atm-Machine-System
```

---

## Install Dependencies

```bash
pip install flask pyserial
```

---

## Run Backend Server

```bash
python main.py
```

---

## Configure Database

1. Install Microsoft SQL Server
2. Open SQL Server Management Studio (SSMS)
3. Restore the provided `.bak` database file
4. Update database connection settings in `db.py`

---

# Screenshots

## ATM CAD Design

```md
![ATM CAD Design](screenshots/atm_frame.png)
```

---

## ATM Interface

```md
![ATM Interface](screenshots/interface.png)
```

---

# Demo Video

```md
[Watch Demo](YOUR_VIDEO_LINK)
```

---

# Future Improvements

- AI-powered fraud detection
- Cloud-hosted banking system
- Mobile application
- Smart financial analytics
- Biometric authentication
- Enhanced cybersecurity
- Multi-user banking support

---

# Author

Mohamed Anwar

AI Engineering Student

---

# License

This project is for educational and research purposes only.
