1. Clone the Repository
git clone https://github.com/cathicath/catbooks.git
cd catbooks

2. Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure the Database
Ensure MySQL is running and create the database manually if needed:
CREATE DATABASE catbooks_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Then, import the database schema:
mysql -u root -p catbooks_db < catbooks.sql

5. Update Database Credentials in app.py
Modify app.py to include your database credentials:
# Database Connection
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="catbooks_db",
    charset="utf8mb4",
    collation="utf8mb4_unicode_ci"
)
cursor = conn.cursor()

6. Run the Application
python3 app.py

The application will be available at:
http://127.0.0.1:5000
