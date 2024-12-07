# **📘 ChatSystem**

A **Django-based chat system** that allows users to create and manage threads, messages, and participants. The system also supports JWT-based authentication, UUIDs for user identification, and customizable token expiry times.

---

## **📋 Features**
- **User Authentication**: Custom user model with UUID as the primary key.  
- **JWT Authentication**: Token-based authentication with customizable token expiration times.  
- **Chat System**: Threaded chat system for entities like `Orders`, `Suppliers`, `Payments`, etc.  
- **CRUD Operations**: Full CRUD for Threads, Messages, and Participants.  

---

## **🚀 Prerequisites**
Make sure you have the following installed on your system:
- **Python** (>= 3.8)
- **Git** (latest version)
- **PostgreSQL** (or any other preferred SQL database)
- **Pip** (Python package manager)
- **Virtual Environment** (optional but recommended)

---

## **💻 Local Development Setup**

Follow these steps to set up the project on your local machine.

---

### **1️⃣ Clone the Repository**
Clone the repository from GitHub:
```bash
git clone https://github.com/rajesh80879/Chat_system.git
cd Chat_system


2️⃣Create a Virtual Environment
python -m venv venv
venv\Scripts\activate

python3 -m venv venv
source venv/bin/activate

3️⃣Install Dependencies
pip install -r requirements.txt

4️⃣Set up the Database
Create a .env file in the root directory and add the following configuration:

SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=*

DB_ENGINE=django.db.backends.postgresql
DB_NAME=chat_system
DB_USER=chat_user
DB_PASSWORD=chat_password
DB_HOST=127.0.0.1
DB_PORT=5432


5️⃣ Run Database Migrations

python manage.py makemigrations
python manage.py migrate


6️⃣ Create a Superuser
python manage.py createsuperuser


7️⃣ Run the Application
python manage.py runserver
Access the app in your browser at:
http://127.0.0.1:8000/

🧪 Testing the Application
python manage.py test


🧾 Available Commands
Command	Description
python manage.py makemigrations	Create new migrations
python manage.py migrate	Apply the migrations
python manage.py createsuperuser	Create a superuser
python manage.py runserver	Run the development server
python manage.py test	Run all tests
