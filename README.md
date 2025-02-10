# catbooks

CatBooks - Web Application

This is a vulnerable web application designed for security testing and penetration testing exercises. The application contains SQL injection vulnerabilities, authentication flaws, and other security misconfigurations.




Getting Started
This repository contains the obfuscated version of the web application, ensuring that the source code remains hidden while still allowing for penetration testing.

Prerequisites

Make sure you have the following installed:

Python 3.12 or later
MariaDB or MySQL
pip (Python package manager)



Installation and Setup

1. Clone the Repository
git clone https://github.com/cathicath/catbooks.git
cd catbooks

2. Install Dependencies
pip install -r requirements.txt

3. Setup the Database
The database is stored in an encoded format for obfuscation. It will be automatically decoded on the first run. Make sure MariaDB or MySQL is running before starting the application.




Running the Application

Start the web application with the following command:
./dist/app

If you get a permission error, run:
chmod +x dist/app
./dist/app

The Flask server will start on http://127.0.0.1:5000.




Troubleshooting

- If you see a "Template Not Found" error, make sure that the dist/templates/ and dist/static/ directories exist and were included during the build process.
- If you get database errors, ensure that MariaDB or MySQL is running and that catbooks.db exists in the project directory.

