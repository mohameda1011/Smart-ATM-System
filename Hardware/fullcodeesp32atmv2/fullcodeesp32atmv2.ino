#include <Keypad.h>
#include <SPI.h>
#include <MFRC522.h>

// ================== PIN CONFIG ==================
#define LED_PIN 2
#define BUZZER 21

// Buttons
#define BTN1 17    
#define BTN2 4
#define BTN3 16
#define GREEN_LED 15

// RFID
#define SS_PIN 5
#define RST_PIN 22
MFRC522 rfid(SS_PIN, RST_PIN);

// ================== KEYPAD ==================
const byte ROWS = 4;
const byte COLS = 3;

char keys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte rowPins[ROWS] = {33, 12, 14, 26};
byte colPins[COLS] = {25,32, 27};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// ================== VARIABLES ==================
String inputBuffer = "";

// =================================================
// ================= FUNCTIONS =====================
// =================================================

// 🔔 Buzzer
void buzzerBeep(int duration = 150) {
  digitalWrite(BUZZER, HIGH);
  delay(duration);
  digitalWrite(BUZZER, LOW);
}

// 💡 LED
void ledOn() {
  digitalWrite(LED_PIN, HIGH);
}

void ledOff() {
  digitalWrite(LED_PIN, LOW);
}


void greenLedOn() {
  digitalWrite(GREEN_LED, HIGH);
}

void greenLedOff() {
  digitalWrite(GREEN_LED, LOW);
}



// 🐍 Send to Python
void sendToPython(String type, String data) {
  Serial.print(type);
  Serial.print(":");
  Serial.println(data);
}

// 📟 Keypad
void handleKeypad() {
  char key = keypad.getKey();

  if (key) {
    sendToPython("KEYPAD", String(key));

    // feedback
    
    buzzerBeep(50);
    
  }
}

// 📡 RFID
void handleRFID() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i], HEX);
  }

  sendToPython("RFID", uid);

  buzzerBeep(200);

  rfid.PICC_HaltA();
}

// 🔘 Buttons
void handleButtons() {

  if (digitalRead(BTN1) == LOW) {
    sendToPython("BUTTON", "1");
    buzzerBeep(100);
    delay(200);
  }

  if (digitalRead(BTN2) == LOW) {
    sendToPython("BUTTON", "2");
    buzzerBeep(100);
    delay(200);
  }

  if (digitalRead(BTN3) == LOW) {
    sendToPython("BUTTON", "3");
    buzzerBeep(100);
    delay(200);
  }
}


// 🎛️ Master LED Controller
// pin: LED_PIN (Red) or GREEN_LED
// doBlink: true (blinks) or false (solid light)
// blinkSpeed: Time between blinks in milliseconds
// totalTime: Total time the LED stays on in milliseconds
void controlLED(int pin, bool doBlink, int blinkSpeed, int totalTime) {
  if (doBlink) {
    int timePassed = 0;
    while (timePassed < totalTime) {
      digitalWrite(pin, HIGH);
      delay(blinkSpeed);
      digitalWrite(pin, LOW);
      delay(blinkSpeed);
      timePassed += (blinkSpeed * 2);
    }
  } else {
    // Go straight on (Solid)
    digitalWrite(pin, HIGH);
    delay(totalTime);
    digitalWrite(pin, LOW);
  }
}



// 📥 Receive commands from Python
void handleSerialCommands() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();   // removes \r, spaces, etc.

    Serial.print("Received: ");
    Serial.println(cmd);

    if (cmd.equalsIgnoreCase("LED:ON")) {
      ledOn();
      Serial.println("LED TURNED ON");
    }
    else if (cmd.equalsIgnoreCase("LED:OFF")) {
      ledOff();
      Serial.println("LED TURNED OFF");
    }

         else if (cmd.equalsIgnoreCase("GREEN:ON")) {
      greenLedOn();
      Serial.println("GREEN LED TURNED ON");
    }
    else if (cmd.equalsIgnoreCase("GREEN:OFF")) {
      greenLedOff();
      Serial.println("GREEN LED TURNED OFF");
    }
    else if (cmd.equalsIgnoreCase("BUZZER")) {
      buzzerBeep(200);
      Serial.println("BUZZER OK");
    }


    else if (cmd.equalsIgnoreCase("TX:SUCCESS")) {
      // SUCCESS: Only Green LED (2 seconds solid)
      greenLedOn(); 
      delay(2000);
      greenLedOff();
      Serial.println("SUCCESS LED OK");
    }
    else if (cmd.equalsIgnoreCase("TX:FAIL")) {
      // FAIL: Only Red LED (Blinks 5 times)
      for(int i = 0; i < 5; i++) { 
        ledOn();
        delay(200);
        ledOff();
        delay(200);
      }
      Serial.println("FAIL LED OK");
    }
    else if (cmd.equalsIgnoreCase("EXIT:BEEP")) {
      // GOODBYE: Only Buzzer (4 slow beeps)
      for(int i = 0; i < 4; i++) { 
        buzzerBeep(250); 
        delay(250);      
      }
      Serial.println("EXIT BEEP OK");
    }

    else {
      Serial.println("UNKNOWN CMD");
    }
  }
}

// =================================================
// ================= SETUP ==========================
// =================================================

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);
  pinMode(BTN3, INPUT_PULLUP);

  SPI.begin();
  rfid.PCD_Init();

  Serial.println("ATM ESP32 READY");
}

// =================================================
// ================= LOOP ===========================
// =================================================

void loop() {
  handleKeypad();
  handleRFID();
  handleButtons();
  handleSerialCommands();
}