import sqlite3

# 1️⃣ Connect to database
connection = sqlite3.connect("data/business.db")

# 2️⃣ Create cursor
cursor = connection.cursor()


# ==============================
# CUSTOMERS TABLE
# ==============================

# 3️⃣ Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    region TEXT
)
""")

# 4️⃣ Customer data
customers = [
    (1, "ABC Electronics", "West"),
    (2, "XYZ Retail", "North"),
    (3, "PQR Stores", "South"),
    (4, "Tech World", "West"),
    (5, "Smart Mart", "East")
]

# 5️⃣ Insert customers
cursor.executemany("""
INSERT OR IGNORE INTO customers
(customer_id, customer_name, region)
VALUES (?, ?, ?)
""", customers)


# ==============================
# PRODUCTS TABLE
# ==============================

# 6️⃣ Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

# 7️⃣ Product data
products = [
    (1, "Laptop", "Electronics", 50000),
    (2, "Smartphone", "Electronics", 30000),
    (3, "Office Chair", "Furniture", 8000),
    (4, "Desk", "Furniture", 12000),
    (5, "Headphones", "Electronics", 3000)
]

# 8️⃣ Insert products
cursor.executemany("""
INSERT OR IGNORE INTO products
(product_id, product_name, category, price)
VALUES (?, ?, ?, ?)
""", products)


# ==============================
# SAVE CHANGES
# ==============================

# 9️⃣ Save everything
connection.commit()

print("Customers and products added successfully!")


# ==============================
# TEST CUSTOMERS
# ==============================

# 🔟 Get all customers
cursor.execute("SELECT * FROM customers")

customers_data = cursor.fetchall()

print("\nCustomers in database:")

for customer in customers_data:
    print(customer)


# ==============================
# TEST FILTER
# ==============================

# 1️⃣1️⃣ Find West customers
cursor.execute("""
SELECT * FROM customers
WHERE region = 'West'
""")

west_customers = cursor.fetchall()

print("\nCustomers from West region:")

for customer in west_customers:
    print(customer)


# ==============================
# TEST PRODUCTS
# ==============================

# 1️⃣2️⃣ Get all products
cursor.execute("SELECT * FROM products")

products_data = cursor.fetchall()

print("\nProducts in database:")

for product in products_data:
    print(product)

# ==============================
# ORDERS TABLE
# ==============================

# 1️⃣ Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

# 2️⃣ Order data
orders = [
    (1001, 1, "2026-01-05"),
    (1002, 2, "2026-01-08"),
    (1003, 3, "2026-01-15"),
    (1004, 1, "2026-02-03"),
    (1005, 4, "2026-02-10"),
    (1006, 5, "2026-02-18"),
    (1007, 1, "2026-03-04"),
    (1008, 2, "2026-03-10"),
    (1009, 3, "2026-03-15"),
    (1010, 4, "2026-03-20")
]

# 3️⃣ Insert orders
cursor.executemany("""
INSERT OR IGNORE INTO orders
(order_id, customer_id, order_date)
VALUES (?, ?, ?)
""", orders)

# 4️⃣ Save changes
connection.commit()

print("\nOrders added successfully!")

# ==============================
# ORDER ITEMS TABLE
# ==============================

# 1️⃣ Create order_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")
# 2️⃣ Order item data
order_items = [
    (1, 1001, 1, 1),
    (2, 1001, 5, 2),
    (3, 1002, 2, 1),
    (4, 1002, 5, 1),
    (5, 1003, 3, 2),
    (6, 1004, 1, 1),
    (7, 1005, 4, 1),
    (8, 1006, 2, 2),
    (9, 1007, 1, 2),
    (10, 1007, 5, 1),
    (11, 1008, 2, 1),
    (12, 1009, 3, 1),
    (13, 1010, 4, 2)
]

# 3️⃣ Insert order items
cursor.executemany("""
INSERT OR IGNORE INTO order_items
(order_item_id, order_id, product_id, quantity)
VALUES (?, ?, ?, ?)
""", order_items)

# 4️⃣ Save changes
connection.commit()

print("\nOrder items added successfully!")

# ==============================
# REVENUE ANALYSIS
# ==============================

# 1️⃣ Calculate revenue for each order
cursor.execute("""
SELECT
    order_items.order_id,
    products.product_name,
    order_items.quantity,
    products.price,
    order_items.quantity * products.price AS revenue
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
""")

# 2️⃣ Get results
revenue_data = cursor.fetchall()

# 3️⃣ Display results
print("\nRevenue details:")

# 4️⃣ Print each result
for row in revenue_data:
    print(row)
    # ==============================
# TOTAL REVENUE
# ==============================

# 1️⃣ Calculate total revenue
cursor.execute("""
SELECT SUM(order_items.quantity * products.price)
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
""")

# 2️⃣ Get result
total_revenue = cursor.fetchone()[0]

# 3️⃣ Display result
print("\nTotal Revenue:")
print(f"₹{total_revenue:,.2f}")

# ==============================
# MONTHLY REVENUE ANALYSIS
# ==============================

# 1️⃣ Calculate revenue month-wise
cursor.execute("""
SELECT
    strftime('%Y-%m', orders.order_date) AS month,
    SUM(order_items.quantity * products.price) AS revenue
FROM orders
JOIN order_items
ON orders.order_id = order_items.order_id
JOIN products
ON order_items.product_id = products.product_id
GROUP BY month
ORDER BY month
""")

# 2️⃣ Get results
monthly_revenue = cursor.fetchall()

# 3️⃣ Display results
print("\nMonthly Revenue:")

# 4️⃣ Print each month
for month, revenue in monthly_revenue:
    print(f"{month} → ₹{revenue:,.2f}")
    
# ==============================
# CATEGORY-WISE REVENUE
# ==============================

# 1️⃣ Calculate revenue by category
cursor.execute("""
SELECT
    products.category,
    SUM(order_items.quantity * products.price) AS revenue
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
GROUP BY products.category
ORDER BY revenue DESC
""")

# 2️⃣ Get results
category_revenue = cursor.fetchall()

# 3️⃣ Display results
print("\nCategory-wise Revenue:")

# 4️⃣ Print each category
for category, revenue in category_revenue:
    print(f"{category} → ₹{revenue:,.2f}") 
    
# ==============================
# TOP PRODUCTS BY REVENUE
# ==============================

# 1️⃣ Calculate revenue for each product
cursor.execute("""
SELECT
    products.product_name,
    SUM(order_items.quantity * products.price) AS revenue
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
GROUP BY products.product_id, products.product_name
ORDER BY revenue DESC
""")

# 2️⃣ Get results
product_revenue = cursor.fetchall()

# 3️⃣ Display results
print("\nProduct-wise Revenue:")

# 4️⃣ Print each product
for product, revenue in product_revenue:
    print(f"{product} → ₹{revenue:,.2f}")

# ==============================
# CUSTOMER-WISE REVENUE
# ==============================

# 1️⃣ Calculate revenue for each customer
cursor.execute("""
SELECT
    customers.customer_name,
    SUM(order_items.quantity * products.price) AS revenue
FROM orders
JOIN customers
ON orders.customer_id = customers.customer_id
JOIN order_items
ON orders.order_id = order_items.order_id
JOIN products
ON order_items.product_id = products.product_id
GROUP BY customers.customer_id, customers.customer_name
ORDER BY revenue DESC
""")

# 2️⃣ Get results
customer_revenue = cursor.fetchall()

# 3️⃣ Display results
print("\nCustomer-wise Revenue:")

# 4️⃣ Print each customer
for customer, revenue in customer_revenue:
    print(f"{customer} → ₹{revenue:,.2f}")
    
# ==============================
# REGION-WISE REVENUE
# ==============================

# 1️⃣ Calculate revenue by region
cursor.execute("""
SELECT
    customers.region,
    SUM(order_items.quantity * products.price) AS revenue
FROM customers
JOIN orders
ON customers.customer_id = orders.customer_id
JOIN order_items
ON orders.order_id = order_items.order_id
JOIN products
ON order_items.product_id = products.product_id
GROUP BY customers.region
ORDER BY revenue DESC
""")

# 2️⃣ Get results
region_revenue = cursor.fetchall()

# 3️⃣ Display results
print("\nRegion-wise Revenue:")

# 4️⃣ Print each region
for region, revenue in region_revenue:
    print(f"{region} → ₹{revenue:,.2f}")
# ==============================
# CLOSE DATABASE
# ==============================

# 1️⃣3️⃣ Close ONLY at the very end
connection.close()












