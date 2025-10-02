CREATE DATABASE pos_system;
USE pos_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(100) not null,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    address varchar(100) not null,
    email VARCHAR(100),
    role varchar(20) NOT NULL
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand_type VARCHAR(50),
    stock_boxes INT DEFAULT 0,
    pieces_per_box INT DEFAULT 1,
    price DECIMAL(10,2),
    expiry_date DATE,
    category VARCHAR(50),
    image VARCHAR(255) DEFAULT 'placeholder.png',
    pieces INT DEFAULT 0
);

-- Insert data 
INSERT INTO products (name, brand_type, category, stock_boxes, pieces_per_box, price, expiry_date, image)
VALUES 
('Squalane Cleanser 50ml', 'Skincare', 'Cleansers', 10, 12, 950.00, '2026-12-31', 'squalane.png'),
('Glycolic Acid 7% Toning Solution', 'Skincare', 'Cleansers', 8, 10, 1050.00, '2026-11-30', 'GlycolicAcid.png'),
('Salicylic Acid 2% Solution', 'Skincare', 'Cleansers', 5, 10, 1100.00, '2026-10-31', 'SalicylicAcid.png'),
('Glucoside Foaming Cleanser', 'Skincare', 'Cleansers', 6, 10, 1000.00, '2026-10-15', 'glucosidefoamingcleanser.png'),
('Alpha Arbutin 2% + HA', 'Skincare', 'Cleansers', 7, 12, 1150.00, '2026-09-30', 'Alpha Arbutin 2% + HA.png'),
('Azelaic Acid Suspension 10%', 'Skincare', 'Cleansers', 6, 8, 1200.00, '2026-08-30', 'AzelaicAcidSuspension.png'),
('Lactic Acid 5% + HA', 'Skincare', 'Cleansers', 4, 6, 950.00, '2026-12-20', 'lacticAcid5%.png'),
('Natural Moisturizing Factors + HA 30ml', 'Skincare', 'Moisturizers', 10, 12, 900.00, '2026-12-31', 'NaturalMoisturizing.png'),
('Natural Moisturizing Factors + HA 100ml', 'Skincare', 'Moisturizers', 6, 10, 1350.00, '2026-11-30', 'natural-moisturizing+HA 100ml.png'),
('Aloe + Panthenol Cream', 'Skincare', 'Moisturizers', 7, 10, 1100.00, '2026-10-31', 'AloePanthenolHydratingGel.png'),
('Beta Glucan Daily Moisturizer', 'Skincare', 'Moisturizers', 5, 8, 1200.00, '2026-09-30', 'beta glucan.png'),
('Hydration Support Serum', 'Skincare', 'Moisturizers', 4, 6, 1500.00, '2026-08-31', 'hydrating.png'),
('B5 + Glycerin Gel', 'Skincare', 'Moisturizers', 6, 8, 1300.00, '2026-11-15', 'B5glycerinegel.png'),
('Hydrating Light Cream', 'Skincare', 'Moisturizers', 8, 10, 1000.00, '2026-10-10', 'hydatinglightcream.png'),
('Intense Repair Balm', 'Skincare', 'Moisturizers', 3, 5, 1550.00, '2026-12-20', 'intense liprepair.png'),
('Mineral UV Filters SPF 30 with Antioxidants', 'Skincare', 'Sunscreen', 9, 10, 1400.00, '2026-12-31', 'mineraluvfilters.png'),
('Sunscreen SPF 50 PA+++', 'Skincare', 'Sunscreen', 5, 8, 1600.00, '2026-10-31', 'spf50pa+++.png'),
('Daily UV Defense SPF 30', 'Skincare', 'Sunscreen', 4, 6, 1450.00, '2026-10-15', 'uvdefense.png'),
('Tinted Sunscreen SPF 30', 'Skincare', 'Sunscreen', 5, 10, 1550.00, '2026-09-30', 'tintedspf30.png'),
('Broad Spectrum SPF 40 Lotion', 'Skincare', 'Sunscreen', 6, 10, 1500.00, '2026-09-15', 'broadspecturumlotion.png'),
('UV Moisture Lock SPF 25', 'Skincare', 'Sunscreen', 3, 5, 1350.00, '2026-08-31', 'mosturizerlock.png'),
('Vitamin C Suspension 23% + HA Spheres 2%', 'Skincare', 'Serums', 8, 12, 1800.00, '2026-12-31', 'vitaminCsuspension.png'),
('Niacinamide 10% + Zinc 1%', 'Skincare', 'Serums', 9, 10, 1700.00, '2026-11-30', 'niacinamide.png'),
('Buffet + Copper Peptides 1%', 'Skincare', 'Serums', 6, 6, 2200.00, '2026-10-31', 'buffet.png'),
('Hyaluronic Acid 2% + B5', 'Skincare', 'Serums', 7, 10, 1900.00, '2026-10-15', 'hyaluronic acid.png'),
('Alpha Arbutin 2% + HA', 'Skincare', 'Serums', 5, 8, 1600.00, '2026-09-30', 'alphaarbutin+haserum.png'),
('Lactic Acid 10% + HA', 'Skincare', 'Serums', 5, 10, 1650.00, '2026-09-15', 'lacticacidserum.png'),
('Ascorbyl Glucoside Solution 12%', 'Skincare', 'Serums', 6, 10, 1850.00, '2026-08-30', 'ascorbylglucoside.png'),
('Resveratrol 3% + Ferulic Acid 3%', 'Skincare', 'Serums', 5, 8, 2100.00, '2026-11-20', 'resveratrolserum.png');

UPDATE products
SET pieces = stock_boxes * pieces_per_box
WHERE id > 0;

SELECT name, image ,pieces FROM products;
select * from users;
select * from products;

-- Product Price History (track when price changes)
CREATE TABLE product_price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Bills (each customer transaction)
CREATE TABLE bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,   -- Will store customer_id like CUST1234
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bill Items (items included in each bill)
CREATE TABLE bill_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price_at_sale DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (bill_id) REFERENCES bills(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sales (each product sale, useful for reporting)
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price_at_sale DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
select * from sales;

