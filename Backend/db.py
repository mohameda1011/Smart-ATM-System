import pyodbc
from datetime import datetime

# Your connection string
DB_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=bank_v2;"
    "Trusted_Connection=yes;"
)

def get_connection():
    try:
        return pyodbc.connect(DB_CONN_STR)
    except Exception as e:
        print(f"Database Error: {e}")
        return None

# 1. Check if the RFID exists in the Account table
# 1. Check if the RFID exists and get the owner's name
def verify_rfid(rfid_uid):
    conn = get_connection()
    if not conn: return None
    cursor = conn.cursor()
    
    # Joining Account and Customer to get the name based on the RFID
    query = """
        SELECT c.Customer_Name 
        FROM Account a
        JOIN Customer c ON a.customer_id = c.customer_id
        WHERE a.rfid_uid = ?
    """
    cursor.execute(query, (rfid_uid,))
    row = cursor.fetchone()
    conn.close()
    
    # Returns the name (string) if found, otherwise None
    return row.Customer_Name if row else None

# 2. Verify the PIN
def verify_pin(rfid_uid, entered_pin):
    conn = get_connection()
    if not conn: return False
    cursor = conn.cursor()
    
    # Looking for the 'pin_code' column you created
    cursor.execute("SELECT pin_code FROM Account WHERE rfid_uid = ?", (rfid_uid,))
    row = cursor.fetchone()
    conn.close()
    
    return True if row and str(row.pin_code) == str(entered_pin) else False

# 3. Get Account Balance
def get_balance(rfid_uid):
    conn = get_connection()
    if not conn: return 0.0
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM Account WHERE rfid_uid = ?", (rfid_uid,))
    row = cursor.fetchone()
    conn.close()
    
    return float(row.balance) if row else 0.0

# 4. Process Withdraw or Deposit
def execute_transaction(rfid_uid, transaction_type, amount):
    conn = get_connection()
    if not conn: return False, "Connection failed"
    cursor = conn.cursor()
    
    try:
        # Get the account info directly using the RFID
        cursor.execute("SELECT account_id, balance FROM Account WHERE rfid_uid = ?", (rfid_uid,))
        row = cursor.fetchone()
        
        if not row:
            return False, "Account not found."
            
        account_id = row.account_id
        current_balance = float(row.balance)
        amount = float(amount)
        
        if transaction_type == 'withdraw' and current_balance < amount:
            return False, "Insufficient funds."
            
        new_balance = current_balance - amount if transaction_type == 'withdraw' else current_balance + amount
        
        # Update the Account Balance
        cursor.execute("UPDATE Account SET balance = ? WHERE account_id = ?", (new_balance, account_id))
        
        # Log the transaction
        current_time = datetime.now()
        cursor.execute("""
            INSERT INTO [Transactions] (Transaction_type, Amount, time, Account_id) 
            VALUES (?, ?, ?, ?)
        """, (transaction_type, amount, current_time, account_id))
        
        conn.commit() 
        return True, "Transaction successful."
        
    except Exception as e:
        conn.rollback() 
        print(f"Transaction Error: {e}")
        return False, "System error."
    finally:
        conn.close()