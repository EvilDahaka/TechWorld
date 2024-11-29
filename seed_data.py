
from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()


    conn.execute('''INSERT INTO products (name, price, specifications, image, tag) VALUES
('Gaming Laptop', 1200.00, 'Intel i7, 16GB RAM, 512GB SSD, NVIDIA GTX 1660Ti', NULL, 'pc'),
('Wireless Mouse', 25.99, '2.4GHz, Optical, 1600 DPI', NULL, 'accessoires'),
('Smartphone X', 799.00, '128GB, OLED Display, Dual Camera', NULL, 'phone'),
('Mechanical Keyboard', 89.99, 'Cherry MX Red switches, RGB Lighting', NULL, 'accessoires'),
('Noise Cancelling Headphones', 199.00, 'Bluetooth, 20h battery life, ANC', NULL, 'accessoires'),
('Ultra HD Monitor', 349.00, '27", 4K Resolution, IPS Panel', NULL, 'pc'),
('Smartphone Charger', 15.00, 'Fast Charging, USB-C', NULL, 'accessoires'),
('Graphics Tablet', 129.99, '10"x6", 8192 Pressure Levels, USB', NULL, 'pc'),
('Smartwatch', 179.00, 'Heart Rate Monitor, GPS, 5ATM Water Resistance', NULL, 'phone'),
('External Hard Drive', 89.00, '1TB, USB 3.0', NULL, 'accessoires');
''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")