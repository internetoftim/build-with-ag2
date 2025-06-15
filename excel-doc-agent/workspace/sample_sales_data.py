import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample sales data
np.random.seed(42)  # For reproducibility

# Generate dates for the last 12 months
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Create product categories and products
categories = ['Electronics', 'Clothing', 'Home Goods', 'Office Supplies']
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor'],
    'Clothing': ['T-shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
    'Home Goods': ['Sofa', 'Bed', 'Table', 'Chair', 'Lamp'],
    'Office Supplies': ['Pen', 'Notebook', 'Stapler', 'Printer', 'Desk']
}

# Create regions and cities
regions = {
    'North': ['New York', 'Boston', 'Chicago'],
    'South': ['Miami', 'Atlanta', 'Dallas'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle'],
    'East': ['Philadelphia', 'Washington DC', 'Baltimore']
}

# Generate random sales data
data = []
for _ in range(1000):
    date = np.random.choice(dates)
    category = np.random.choice(categories)
    product = np.random.choice(products[category])
    region = np.random.choice(list(regions.keys()))
    city = np.random.choice(regions[region])
    quantity = np.random.randint(1, 20)
    unit_price = np.random.uniform(10, 1000) if category == 'Electronics' else \
                np.random.uniform(10, 200) if category == 'Clothing' else \
                np.random.uniform(50, 500) if category == 'Home Goods' else \
                np.random.uniform(5, 50)
    total_price = quantity * unit_price
    
    data.append({
        'Date': date,
        'Category': category,
        'Product': product,
        'Region': region,
        'City': city,
        'Quantity': quantity,
        'UnitPrice': round(unit_price, 2),
        'TotalPrice': round(total_price, 2)
    })

# Create DataFrame
df = pd.DataFrame(data)

# Add some calculated columns
df['Month'] = df['Date'].dt.month_name()
df['Quarter'] = 'Q' + df['Date'].dt.quarter.astype(str)
df['Year'] = df['Date'].dt.year

# Save to Excel
df.to_excel('sample_sales_data.xlsx', index=False)
print("Sample sales data Excel file created: sample_sales_data.xlsx")
