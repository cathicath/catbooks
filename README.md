# CatBooks - Online Bookstore  
  
CatBooks is a web-based bookstore built with Flask, MySQL, and Docker. It allows users to browse books, manage reviews, and provides an admin panel for book management.  
  
## Features  
- Browse available books  
- User authentication system  
- Admin panel for managing books and reviews  
- Responsive design  
- Dockerized setup for easy deployment  
- Virtual environment support (`venv`)  
  
---  
  
## Installation  
  
### 1. Clone the repository  
  
git clone https://github.com/cathicath/catbooks.git  
cd catbooks  

### 2. Create and activate a virtual environment  
  
Before running the application, ensure you are using a virtual environment:  
  
python3 -m venv venv  
source venv/bin/activate  
  
## Setup and Run  
  
### 1. Install Dependencies  
  
pip install -r requirements.txt  
  
### 2. Ensure Docker is installed
  
## Running with Docker  
  
### 1. Start the application  
  
docker-compose up --build -d  
  
This will start both the Flask application and the MySQL database in the background.  
  
### 2. Import the database schema and books data  
  
Once the database container is running, execute the following commands to load the database structure (catbooks.sql) and add books to the shop (books.sql):  
  
docker exec -i catbooks_mysql mysql -u root -p catbooks_db < catbooks.sql  
docker exec -i catbooks_mysql mysql -u root -p catbooks_db < books.sql  
  
When prompted, enter the MySQL root password (found in .env).  
  
### 3. Restart the application  
  
docker restart catbooks_app  
  
## Access the Application
  
After setup, open your browser and go to:  
http://localhost:5000  
  

