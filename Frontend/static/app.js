// --- State Variables ---
let currentState = "IDLE"; 
let currentInput = "";
let currentRFID = null;
let currentMessage = "Please tap your card.";

const displayTitle = document.getElementById("display-title");
const displayMessage = document.getElementById("display-message");
const displayInput = document.getElementById("display-input");

function renderScreen() {
    displayInput.innerText = currentState === "PIN" ? "*".repeat(currentInput.length) : currentInput;
    displayMessage.innerText = currentMessage;

    const titles = {
        "IDLE": "Welcome", "PIN": "Authentication", "MENU": "Main Menu",
        "WITHDRAW": "Withdraw Cash", "DEPOSIT": "Deposit Cash", "BALANCE": "Balance Inquiry",
        "SUCCESS": "Complete", "ERROR": "Error", "EXIT": "Goodbye"
    };
    displayTitle.innerText = titles[currentState] || "ATM";

    if (["PIN", "WITHDRAW", "DEPOSIT"].includes(currentState)) {
        displayInput.style.display = "block";
    } else {
        displayInput.style.display = "none";
    }

    const logo = document.getElementById("uni-logo");
    logo.style.display = currentState === "IDLE" ? "block" : "none";

}

async function processHardwareInput(type, value) {
    // 1. Handle RFID Login
    if (type === 'rfid' && currentState === "IDLE") {
        currentMessage = "Processing...";
        renderScreen();
        try {
            const res = await fetch('/api/verify_rfid', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rfid_uid: value })
            });
            const data = await res.json();
            if (data.success) {
                currentRFID = value;
                currentState = "PIN";
                currentInput = "";
                currentMessage = `Welcome, ${data.name}!\nEnter PIN:`;
            } else {
                showError("Invalid Card.");
            }
        } catch (e) { showError("System Error."); }
        renderScreen();
        return;
    }

    // 2. Handle Keypad
    if (type === 'keypad') {
        if (["PIN", "WITHDRAW", "DEPOSIT"].includes(currentState)) {
            currentInput += value;
        } else if (currentState === "MENU") {
            if (value === '1') { currentState = "WITHDRAW"; currentInput = ""; currentMessage = "Amount:\n\n(Press Continue when done)"; }
            if (value === '2') { currentState = "DEPOSIT"; currentInput = ""; currentMessage = "Amount:\n\n(Press Continue when done)"; }
            if (value === '3') { checkBalance(); return; }
            if (value === '4') { exitSession(); return; }
        } else if (currentState === "SUCCESS" || currentState === "ERROR" || currentState === "BALANCE") {
            // THIS IS THE MISSING LOGIC!
            if (value === '1') { 
                currentState = "MENU"; 
                currentInput = ""; 
                currentMessage = "1. Withdraw\n2. Deposit\n3. Balance\n4. Exit"; 
            }
            if (value === '2') { exitSession(); return; }
        }
        renderScreen();
    }

    // 3. Handle Actions
    if (type === 'action') {
        if (value === 'reset') currentInput = "";
        else if (value === 'cancel') exitSession();
        else if (value === 'continue') {
            if (currentState === "PIN") verifyPin();
            else if (["WITHDRAW", "DEPOSIT"].includes(currentState)) processTransaction(currentState.toLowerCase());
        }
        renderScreen();
    }
}

// --- API Helpers ---
async function verifyPin() {
    try {
        const res = await fetch('/api/verify_pin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rfid_uid: currentRFID, pin: currentInput })
        });
        const data = await res.json();
        if (data.success) {
            currentState = "MENU";
            currentInput = "";
            currentMessage = "1. Withdraw\n2. Deposit\n3. Balance\n4. Exit";
        } else {
            currentInput = "";
            currentMessage = "Incorrect PIN. Try again:";
        }
    } catch (e) { showError("System Error"); }
    renderScreen();
}

async function checkBalance() {
    currentState = "BALANCE";
    renderScreen();
    try {
        const res = await fetch('/api/balance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rfid_uid: currentRFID })
        });
        const data = await res.json();
        
        // FIX: Updated text to match your actual working keypad logic!
        currentMessage = `Balance: $${data.balance.toFixed(2)}\n\n1. Menu\n2. Exit`;
    } catch (e) { showError("System Error"); }
    renderScreen();
}

async function processTransaction(type) {
    try {
        const res = await fetch('/api/transaction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rfid_uid: currentRFID, type: type, amount: currentInput })
        });
        const data = await res.json();
        
        if (data.success) {
            currentState = "SUCCESS";
            currentMessage = `${data.message}\n\n`; 
            renderScreen(); // Show 'Please wait' while LED flashes
            
            // Wait exactly 2 seconds for the ESP32 Green LED to finish, THEN show options
            setTimeout(() => {
                currentMessage = `${data.message}\n\n1. Menu\n2. Exit`;
                renderScreen();
            }, 2000);
            
        } else { 
            currentState = "ERROR";
            currentMessage = `${data.message}\n\n)`;
            renderScreen(); // Show 'Please wait' while Red LED flashes
            
            // Wait exactly 2 seconds for the ESP32 Red LED to finish, THEN show options
            setTimeout(() => {
                currentMessage = `${data.message}\n\n1. Menu\n2. Exit`;
                renderScreen();
            }, 2000);
        }
        
    } catch (e) { 
        showError("System Error"); 
    }
}

function showError(msg) {
    currentState = "ERROR";
    currentMessage = `${msg}\n1. Menu\n2. Exit`;
    renderScreen();
}

async function exitSession() {
    // 1. Show the Goodbye screen
    currentState = "EXIT";
    currentMessage = "Thank you for using MNU ATM!";
    renderScreen();

    // 2. Trigger the goodbye beeps on the ESP32
    try {
        await fetch('/api/exit_beep', { method: 'POST' });
    } catch (e) {
        console.error("Could not trigger exit beep");
    }

    // 3. Wait exactly 2 seconds (for the 4 beeps to finish), then go to Welcome page
    setTimeout(() => { 
        location.reload(); 
    }, 2000);
}

// --- Single Polling Loop ---
setInterval(async () => {
    try {
        const response = await fetch('/api/get_hardware_input');
        const data = await response.json();
        if (data && data.type !== null) {
            console.log("Hardware Event:", data);
            processHardwareInput(data.type, data.value);
        }
    } catch (e) {}
}, 500);

renderScreen();