from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def connect_db():
    return sqlite3.connect("database.db")

# 🔸 Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        item TEXT,
        quantity INTEGER,
        total INTEGER
    )
    ''')

    conn.commit()
    conn.close()

create_tables()

# 🔹 Get menu (static for now)
@app.route('/menu', methods=['GET'])
def get_menu():
    menu = [
        {"name": "Coffee", "price": 100},
        {"name": "Cold Coffee", "price": 150},
        {"name": "Latte", "price": 180},
        {"name": "Cappuccino", "price": 200}
    ]
    return jsonify(menu)

# 🔹 Place order
@app.route('/order', methods=['POST'])
def place_order():
    data = request.json

    name = data.get("name")
    item = data.get("item")
    quantity = int(data.get("quantity"))
    total = int(data.get("total"))

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO orders (name, item, quantity, total) VALUES (?, ?, ?, ?)",
        (name, item, quantity, total)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Order placed successfully"})

# 🔹 Get all orders (optional)
@app.route('/orders', methods=['GET'])
def get_orders():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()

    conn.close()

    orders = []
    for row in data:
        orders.append({
            "id": row[0],
            "name": row[1],
            "item": row[2],
            "quantity": row[3],
            "total": row[4]
        })

    return jsonify(orders)


if __name__ == "__main__":
    app.run(debug=True)
