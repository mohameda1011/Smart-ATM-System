# Smart ATM System

A smart ATM simulation system built using Python, Flask, SQL database integration, and serial communication with external hardware devices such as Arduino and RFID readers.

The project combines software engineering, embedded systems, and web technologies to simulate real-world ATM operations.

---

# Features

## Banking Operations
- User authentication
- Balance inquiry
- Deposit money
- Withdraw money
- Transaction processing

## Hardware Integration
- Serial communication support
- Arduino connectivity
- RFID/Card reader integration
- External device interaction

## Web Interface
- Interactive ATM-style UI
- Dynamic frontend using JavaScript
- Responsive design

## Database Management
- Store customer information
- Account management
- Transaction history
- Secure balance updates

---

# Technologies Used

## Backend
- Python
- Flask

## Frontend
- HTML
- CSS
- JavaScript

## Hardware & Communication
- Arduino
- Serial Communication (PySerial)

## Database
- SQL Database

---

# Project Structure

```bash
atm_system_v2/
│
├── main.py                 # Main backend server
├── db.py                   # Database operations
├── serial_reader.py        # Serial communication with hardware
│
├── templates/
│   └── index.html          # Main frontend page
│
├── static/
│   ├── app.js              # Frontend logic
│   ├── style.css           # UI styling
│   └── MNU (1).png         # Images/assets
│
└── __pycache__/            # Python cache files
