Документація REST API для магазину

Базова URL адреса API:
 http://127.0.0.1:5000/api
Endpoints

Товари (Products)

	Запит:
---------------------------------------------------------
GET	/api/products
---------------------------------------------------------
Отримує список всіх доступних товарів.

	Відповідь:
*** json
[
    {
        "id": 1,
        "image": null,
        "name": "Gaming Laptop",
        "price": 1200.0,
        "specifications": "Intel i7, 16GB RAM, 512GB SSD, NVIDIA GTX 1660Ti",
        "tag": "pc"
    },
    {
        "id": 2,
        "image": null,
        "name": "Wireless Mouse",
        "price": 25.99,
        "specifications": "2.4GHz, Optical, 1600 DPI",
        "tag": "accessoires"
    },
    {
        "id": 3,
        "image": null,
        "name": "Smartphone X",
        "price": 799.0,
        "specifications": "128GB, OLED Display, Dual Camera",
        "tag": "phone"
    },
    {
        "id": 4,
        "image": null,
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "specifications": "Cherry MX Red switches, RGB Lighting",
        "tag": "accessoires"
    },
    {
        "id": 5,
        "image": null,
        "name": "Noise Cancelling Headphones",
        "price": 199.0,
        "specifications": "Bluetooth, 20h battery life, ANC",
        "tag": "accessoires"
    },
    {
        "id": 6,
        "image": null,
        "name": "Ultra HD Monitor",
        "price": 349.0,
        "specifications": "27\", 4K Resolution, IPS Panel",
        "tag": "pc"
    },
    {
        "id": 7,
        "image": null,
        "name": "Smartphone Charger",
        "price": 15.0,
        "specifications": "Fast Charging, USB-C",
        "tag": "accessoires"
    },
    {
        "id": 8,
        "image": null,
        "name": "Graphics Tablet",
        "price": 129.99,
        "specifications": "10\"x6\", 8192 Pressure Levels, USB",
        "tag": "pc"
    },
    {
        "id": 9,
        "image": null,
        "name": "Smartwatch",
        "price": 179.0,
        "specifications": "Heart Rate Monitor, GPS, 5ATM Water Resistance",
        "tag": "phone"
    },
    {
        "id": 10,
        "image": null,
        "name": "External Hard Drive",
        "price": 89.0,
        "specifications": "1TB, USB 3.0",
        "tag": "accessoires"
    }
]
***
	Коди статусу:
- 201:  Successfuly
- 500:  Internal Server Error



Замовлення (Orders)

Запит:
---------------------------------------------------------
POST	/api/orders
Content-Type: application/json
---------------------------------------------------------
Створює нове замовлення в системі.

	Тіло запиту:
*** json
{
  "email": "orest@kondatyuk.com",
  "address": "Orestovyi address",
  "cart": {
    "1": {
      "id": 1,
      "quantity": 2,
      "price": 7000.0  // додай ціну
    }
  }
}

***

	Відповідь:
*** json
{
    "message": "Order created successfully"
}
***

	Коди статусу:
- 201:  Order created successfully
- 500:  Internal Server Error
- 400:  Missing required fields





Запит:
---------------------------------------------------------
GET	/api/orders/{order_id}
---------------------------------------------------------
Отримує деталі конкретного замовлення.

	Відповідь:
***json
{
    "items": [
        {
            "id": 1,
            "order_id": 4,
            "product_id": 3,
            "quantity": 3
        },
        {
            "id": 2,
            "order_id": 4,
            "product_id": 4,
            "quantity": 4
        },
        {
            "id": 3,
            "order_id": 4,
            "product_id": 5,
            "quantity": 2
        },
        {
            "id": 4,
            "order_id": 4,
            "product_id": 6,
            "quantity": 1
        },
        {
            "id": 5,
            "order_id": 4,
            "product_id": 7,
            "quantity": 4
        },
        {
            "id": 6,
            "order_id": 4,
            "product_id": 8,
            "quantity": 1
        }
    ],
    "order": {
        "address": "вулиця Львівська, 63",
        "date": "2024-12-04 15:39:09",
        "email": "pendejoJOJO@gmail.com",
        "id": 4,
        "status": "New",
        "total_price": 16049.85
    }
}
***
	Коди статусу:
- 200:  Successfully
- 500:  Internal Server Error
- 404:  Order not found


Запит:
---------------------------------------------------------
PUT	/api/orders/{order_id}
Content-Type: application/json
---------------------------------------------------------
Оновлює статус вибраного замовлення.

	Тіло запиту:
{
  "status": "Shipped"
}

	Відповідь:
***json
{
    "message": "Order updated successfully"
}
***
	Коди статусу:
- 200:  Order updated successfully
- 500:  Internal Server Error
- 400:  Status is required



Запит:
---------------------------------------------------------
DELETE	/api/orders/{order_id}
---------------------------------------------------------
Видаляє вибране замовлення.

	Відповідь:
***json
{
    "message": "Order deleted successfully"
}
***
	
	Коди статусу:
- 200:  Order deleted successfully
- 500:  Internal Server Error


Відгуки (Feedback)

Запит:
---------------------------------------------------------
GET	/api/feedback
---------------------------------------------------------
Отримує список всіх відгуків.

	Відповідь:
***json
 [
    {
        "email": "john.doe@example.com",
        "id": 2,
        "message": "This is a feedback message.",
        "name": "John Doe"
    },
    {
        "email": "ivan@example.com",
        "id": 3,
        "message": "Дуже задоволений вашим сервісом!",
        "name": "Іван Іванов"
    }
]
***
	Коди статусу:
- 200:  Successfully
- 500:  Internal Server Error

Запит:
---------------------------------------------------------
POST	/api/feedback
Content-Type: application/json
---------------------------------------------------------
Надсилає відгук користувача.
	Тіло запиту:
{
    "name": "Я Кондратюк",
    "email": "yotik@example.com",
    "message": "nice phone!"
    
}

	Відповідь:
***json
{
    "message": "Feedback submitted successfully"
}
***
	Коди статусу:
- 201:  Feedback submitted successfully
- 400: All fields are required
- 500:  Internal Server Error

Запит:
---------------------------------------------------------
DELETE  /api/feedback/{feedback_id}
---------------------------------------------------------
Видаляє вибраний відгук.
	Відповідь:
***json
{
    "message": "Feedback deleted successfully"
}
***
	Коди статусу:
- 201:  Feedback deleted successfully
- 404:  Feedback not found
- 500:  Internal Server Error