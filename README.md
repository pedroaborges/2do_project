# **🐍 DJANGO DOCUMENTATION 🐍**

## **What's Django and tools?**

### **• Web framework in Python (front-end and back-end)**
### **• User Authentication**
### **• Admin Panel**
### **• ORM - Object-Relational Mapping (relational object data base)**
### **• Templates (front-end)**
### **• Security Systems (SQL injections, etc.)**

##

## **MVT Architecture**

### **1. Model: represents the project's data and how they are saved**
### **2. View: contains the project's logic**
### **3. Template: defines how the project will be displayed (HTML, CSS, etc.)**

##

## **How to install and run a Django project**

### **1. Create virtual environment**
`python -m venv venv`

### **2. Authorize activation command for Windows**
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### **3. Activate virtual environment**
`venv\Scripts\activate`

### **4. Install Django in virtual environment**
`pip install django`

### **5. Create Django Project**
`django-admin startproject projectName`

### **6. Run development server**
`python manage.py runserver`

### **7. Create a super user**
`python manage.py createsuperuser`

##

## **How to run Django project (server)**

### Follow **2, 3 and 6** instructions.

##

## **How to test Django project**
`python manage.py test`

##

## **Data base management**

### **Migrations are files that contains instructions for data base changes.**

### **1. Create migrations (detects the models changes - without apling it)**
`python manage.py makemigrations`

## **2. Aply the migrations (aplies the models changes)**
`python manage.py migrate`

### **3. Show a list of all migrations**
`python manage.py showmigrations`

##

## **Apps**

### **Independent module that implements a specific functionality of project.**

### **Create an app into Django project**
`python manage.py startapp appName`

### **To register it go to `settings.py` and add it to `INSTALLED_APPS` dictionary**

##

## **Integrate AI**

### **Install Gemini API Library in venv**
`pip install -q -U google-genai`

### **Usage**
```python
from google import genai

client = genai.Client(
   api_key="KEY"
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

return response.text
```

##

## **Dependencies**

### **To install all dependencies required**
`pip install -r .\requiments.txt`

##

## **How to use PostgreSQL**

### **Install the PostgreeSQL library**
`pip install psycopg2`

### **Configure the `settings.py` file**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user (default: postgres)',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

### **After all, use the comand**
`python manage.py migrate`