"""
Run this with: python manage.py shell < load_mo_sale_data.py
"""

from catalog.models import Customer, Item, OrderInfo, Stock, OrderLine, Barcode
from datetime import date

print("Starting data load from MO_Sale.sql...")

print("\n1. Inserting customers...")

customers_data = [
    ('Miss', 'Jenny', 'Stones', '27 Rowan Avenue', 'Hightown', 'NT2 1AQ', '023 9876'),
    ('Mr', 'Andrew', 'Stones', '52 The Willows', 'Lowtown', 'LT5 7RA', '876 3527'),
    ('Miss', 'Alex', 'Matthew', '4 The Street', 'Nicetown', 'NT2 2TX', '010 4567'),
    ('Mr', 'Adrian', 'Matthew', 'The Barn', 'Yuleville', 'YV67 2WR', '487 3871'),
    ('Mr', 'Simon', 'Cozens', '7 Shady Lane', 'Oahenham', 'OA3 6QW', '514 5926'),
    ('Mr', 'Neil', 'Matthew', '5 Pasture Lane', 'Nicetown', 'NT3 7RT', '267 1232'),
    ('Mr', 'Richard', 'Stones', '34 Holly Way', 'Bingham', 'BG4 2WE', '342 5982'),
    ('Mrs', 'Ann', 'Stones', '34 Holly Way', 'Bingham', 'BG4 2WE', '342 5982'),
    ('Mrs', 'Christine', 'Hickman', '36 Queen Street', 'Histon', 'HT3 5EM', '342 5432'),
    ('Mr', 'Mike', 'Howard', '86 Dysart Street', 'Tibsville', 'TB3 7FG', '505 5482'),
    ('Mr', 'Dave', 'Jones', '54 Vale Rise', 'Bingham', 'BG3 8GD', '342 8264'),
    ('Mr', 'Richard', 'Neill', '42 Thached way', 'Winersby', 'WB3 6GQ', '505 6482'),
    ('Mrs', 'Laura', 'Hendy', '73 Margeritta Way', 'Oxbridge', 'OX2 3HX', '821 2335'),
    ('Mr', 'Bill', 'ONeill', '2 Beamer Street', 'Welltown', 'WT3 8GM', '435 1234'),
    ('Mr', 'David', 'Hudson', '4 The Square', 'Milltown', 'MT2 6RT', '961 4526'),
]

for title, fname, lname, addressline, town, zipcode, phone in customers_data:
    Customer.objects.create(
        title=title,
        fname=fname,
        lname=lname,
        addressline=addressline,
        town=town,
        zipcode=zipcode,
        phone=phone
    )

print(f"✓ Created {len(customers_data)} customers")

print("\n2. Inserting items...")

items_data = [
    ('Wood Puzzle', 15.23, 21.95),
    ('Rubic Cube', 7.45, 11.49),
    ('Linux CD', 1.99, 2.49),
    ('Tissues', 2.11, 3.99),
    ('Picture Frame', 7.54, 9.95),
    ('Fan Small', 9.23, 15.75),
    ('Fan Large', 13.36, 19.95),
    ('Toothbrush', 0.75, 1.45),
    ('Roman Coin', 2.34, 2.45),
    ('Carrier Bag', 0.01, 0.0),
    ('Speakers', 19.73, 25.32),
    ('Small Ball', None, None),
    ('Large Ball', None, None),
    ('Torus', 2.07, 2.49),
]

for description, cost_price, sell_price in items_data:
    Item.objects.create(
        description=description,
        cost_price=cost_price,
        sell_price=sell_price
    )

print(f"✓ Created {len(items_data)} items")


print("\n3. Inserting orders...")

orders_data = [
    (3, date(2000, 3, 13), date(2000, 3, 17), 2.99),
    (8, date(2000, 6, 23), date(2000, 6, 24), 0.00),
    (15, date(2000, 9, 2), date(2000, 9, 12), 3.99),
    (13, date(2000, 9, 3), date(2000, 9, 10), 2.99),
    (8, date(2000, 7, 21), date(2000, 7, 24), 0.00),
]

for customer_id, date_placed, date_shipped, shipping in orders_data:
    OrderInfo.objects.create(
        customer_id=customer_id,
        date_placed=date_placed,
        date_shipped=date_shipped,
        shipping=shipping
    )

print(f"✓ Created {len(orders_data)} orders")


print("\n4. Inserting order lines...")

orderlines_data = [
    (1, 4, 1),
    (1, 7, 1),
    (1, 9, 1),
    (2, 1, 1),
    (2, 10, 1),
    (2, 7, 2),
    (2, 4, 2),
    (3, 2, 1),
    (3, 1, 1),
    (4, 5, 2),
    (5, 1, 1),
    (5, 3, 1),
]

for orderinfo_id, item_id, quantity in orderlines_data:
    OrderLine.objects.create(
        orderinfo_id=orderinfo_id,
        item_id=item_id,
        quantity=quantity
    )

print(f"✓ Created {len(orderlines_data)} order lines")

print("\n5. Inserting stock records...")

stock_data = [
    (1, 12),
    (2, 2),
    (4, 8),
    (5, 3),
    (7, 8),
    (8, 18),
    (10, 1),
]

for item_id, quantity in stock_data:
    Stock.objects.create(
        item_id=item_id,
        quantity=quantity
    )

print(f"✓ Created {len(stock_data)} stock records")


print("\n6. Inserting barcodes...")

barcodes_data = [
    ('6241527836173', 1),
    ('6241574635234', 2),
    ('6264537836173', 3),
    ('6241527746363', 3),
    ('7465743843764', 4),
    ('3453458677628', 5),
    ('6434564564544', 6),
    ('8476736836876', 7),
    ('6241234586487', 8),
    ('9473625532534', 8),
    ('9473627464543', 8),
    ('4587263646878', 9),
    ('9879879837489', 11),
    ('2239872376872', 11),
]

for barcode_ean, item_id in barcodes_data:
    Barcode.objects.create(
        barcode_ean=barcode_ean,
        item_id=item_id
    )

print(f"✓ Created {len(barcodes_data)} barcodes")


print("\n" + "="*50)
print("DATA LOAD COMPLETE!")
print("="*50)
print(f"Customers:   {Customer.objects.count()}")
print(f"Items:       {Item.objects.count()}")
print(f"Orders:      {OrderInfo.objects.count()}")
print(f"Order Lines: {OrderLine.objects.count()}")
print(f"Stock:       {Stock.objects.count()}")
print(f"Barcodes:    {Barcode.objects.count()}")
print("="*50)
