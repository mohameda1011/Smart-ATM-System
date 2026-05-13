from flask import Flask, render_template, jsonify, request
import serial_reader
import db

app = Flask(__name__)

# Start listening to the ESP32 on COM13
serial_reader.start_serial_thread(port='COM4')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_hardware_input', methods=['GET'])
def api_get_hardware_input():
    # Grab the current state of the hardware event
    event = serial_reader.latest_hardware_event.copy()
    
    if event['type'] is not None:
        # Clear the global event immediately after copying
        serial_reader.latest_hardware_event = {"type": None, "value": None}
        print(f">>> DATA SENT TO WEB: {event}")
        return jsonify(event)
        
    return jsonify({"type": None, "value": None})

# --- Database API Routes ---

@app.route('/api/verify_rfid', methods=['POST'])
def api_verify_rfid():
    data = request.json
    rfid_uid = data.get('rfid_uid')
    name = db.verify_rfid(rfid_uid)
    return jsonify({"success": True, "name": name}) if name else jsonify({"success": False})

@app.route('/api/verify_pin', methods=['POST'])
def api_verify_pin():
    data = request.json
    is_valid = db.verify_pin(data.get('rfid_uid'), data.get('pin'))
    
    # --- NEW LED LOGIC: Flash Green if PIN is correct, Red if wrong ---
    if serial_reader.ser_connection and serial_reader.ser_connection.is_open:
        if is_valid:
            serial_reader.ser_connection.write(b"TX:SUCCESS\n")
        else:
            serial_reader.ser_connection.write(b"TX:FAIL\n")
            
    return jsonify({"success": is_valid})

@app.route('/api/balance', methods=['POST'])
def api_balance():
    balance = db.get_balance(request.json.get('rfid_uid'))
    return jsonify({"success": True, "balance": balance})

@app.route('/api/transaction', methods=['POST'])
def api_transaction():
    data = request.json
    success, message = db.execute_transaction(data.get('rfid_uid'), data.get('type'), data.get('amount'))
    
    # --- NEW LED LOGIC: Flash Green for success, Red for failure (e.g. no funds) ---
    if serial_reader.ser_connection and serial_reader.ser_connection.is_open:
        if success:
            serial_reader.ser_connection.write(b"TX:SUCCESS\n")
        else:
            serial_reader.ser_connection.write(b"TX:FAIL\n")
            
    return jsonify({"success": success, "message": message})


@app.route('/api/exit_beep', methods=['POST'])
def api_exit_beep():
    # Send the goodbye command to the ESP32
    if serial_reader.ser_connection and serial_reader.ser_connection.is_open:
        serial_reader.ser_connection.write(b"EXIT:BEEP\n")
    return jsonify({"success": True})
             
if __name__ == '__main__':
    # use_reloader=False is critical to prevent duplicate serial threads
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)