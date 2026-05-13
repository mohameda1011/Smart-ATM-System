import serial
import threading
import time

latest_hardware_event = {"type": None, "value": None}
ser_connection = None

def read_from_esp32(port='COM4', baudrate=115200):
    global latest_hardware_event, ser_connection
    
    # We moved the 'while True' to the very outside so the loop NEVER dies!
    while True:
        try:
            # 1. Auto-Reconnect if the connection drops
            if ser_connection is None or not ser_connection.is_open:
                ser_connection = serial.Serial(port, baudrate, timeout=1)
                print(f"[*] Connected to ESP32 on {port}")
            
            # 2. Read incoming data
            if ser_connection.in_waiting > 0:
                # errors='ignore' forces Python to ignore electrical noise/junk characters
                line = ser_connection.readline().decode('utf-8', errors='ignore').strip()
                
                if ":" in line:
                    msg_type, msg_value = line.split(":", 1)
                    
                    if msg_type == "KEYPAD":
                        latest_hardware_event = {"type": "keypad", "value": msg_value}
                    elif msg_type == "RFID":
                        latest_hardware_event = {"type": "rfid", "value": msg_value}
                    elif msg_type == "BUTTON":
                        if msg_value == "1": latest_hardware_event = {"type": "action", "value": "continue"}
                        elif msg_value == "2": latest_hardware_event = {"type": "action", "value": "cancel"}
                        elif msg_value == "3": latest_hardware_event = {"type": "action", "value": "reset"}
                        
        except serial.SerialException as e:
            # If the ESP32 physically reboots, Python will wait 2 seconds and try again
            print(f"[!] Connection lost. Reconnecting... ({e})")
            if ser_connection:
                ser_connection.close()
            ser_connection = None
            time.sleep(2)
            
        except Exception as e:
            # Catch any other random errors so the thread stays alive
            print(f"[!] Parse error: {e}")
            
        time.sleep(0.05)

def start_serial_thread(port='COM4'):
    thread = threading.Thread(target=read_from_esp32, args=(port,), daemon=True)
    thread.start()