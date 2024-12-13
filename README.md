Shop & Customer Management Web App

Description:

This web application is developed using the Django framework to manage shop and customer functionalities. It includes APIs for customer registration, login, product management, and order management.

The project is divided into two sections:

- Shop (Admin)
- Customer


Features:

Admin/Shop Features

- Login
- Manage Products (Add, Edit, Delete, View with Average Rating)
- View and Manage Customers List
- View and Update Order Status (Approved/Shipped/Delivered)


Customer Features:

Signup and Login

- Browse Products
- Add Multiple Items to Cart
- Place Orders with Address Management
- View Order Status
- Rate Products


APIs:

- Customer Signup API
- Customer Login API
- Product List API
- User-Specific Orders API (Authentication Required)

Installation:

- Clone the repository:

  git clone

  https://github.com/Shanidh/shop_app_zg.git

- Create a virtual environment and activate it:

  python -m venv env
  .\venv\scripts\activate.ps1

- Install the dependencies:

  pip install -r requirement.txt   
  
- Run migrations:

  python manage.py makemigrations  
  python manage.py migrate

- Start the server:

  python manage.py runserver


How to Use:

For Admin/Shop

- Access the admin panel using the following URL:

  http://127.0.0.1:8000/admin/login/  

For Customer

- The landing page for customers is available at:

  http://127.0.0.1:8000/


API Endpoints:

1. Customer Signup

  URL: /api/customer/signup/
  
  Method: POST
  
  Payload:

  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
  }

2. Customer Login

  URL: /login/api

  Method: POST

  Payload:

  {
    "username": "john_doe",
    "password": "secure_password"
  }


 3. Product List
    
    URL: /product/list/api
    
    Method: GET
    
 4. User-Specific Orders
    
    URL: /orders/api
    
    Method: GET
    
    Authentication Required: Yes


Testing:

- Use Postman or similar tools to test the APIs.
- Login credentials for testing the admin panel can be provided during superuser creation.
    
