import time
import mysql.connector
from mysql.connector import Error

db_config = {
    "host": "db",  # OBS! "db" måste matcha `docker-compose.yml`
    "user": "root",
    "password": "kali123",
}

def wait_for_db():
    """Väntar på att databasen ska vara redo."""
    for _ in range(10):
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                print("✅ MySQL är redo!")
                return connection
        except Error:
            print("⏳ Väntar på att MySQL startar...")
            time.sleep(3)
    raise Exception("❌ Kunde inte ansluta till MySQL.")

try:
    conn = wait_for_db()
    cursor = conn.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS catbooks_db;")
    conn.commit()
    cursor.close()
    conn.close()
    print("🎉 Databasen skapad!")
except Exception as e:
    print(f"❌ Fel vid initiering: {e}")
