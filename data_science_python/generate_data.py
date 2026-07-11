import sys
try:
    import pandas as pd  # type: ignore
    import numpy as np  # type: ignore
except Exception as e:
    print("Required packages not found. Please install dependencies: pandas, numpy")
    print("Error:", e)
    sys.exit(1)

from datetime import datetime, timedelta

print("🚀 High-Frequency Data Generation Start Ho Raha Hai...")

# 1. Configuration Settings
NUM_CUSTOMERS = 15000       # 15k unique customers
NUM_PRODUCTS = 250          # 250 products across categories
NUM_TRANSACTIONS = 600000   # 600k rows (High-Frequency)
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 5, 31)

np.random.seed(42) # For repeatability

# 2. Generate Dim_Customers
print("👥 Generating Customer Dimension...")
customer_ids = [f"CUST_{str(i).zfill(5)}" for i in range(1, NUM_CUSTOMERS + 1)]
channels = ['Social Media', 'Google Ads', 'Direct Organic', 'Affiliate', 'Email Market']
cust_channels = np.random.choice(channels, size=NUM_CUSTOMERS, p=[0.35, 0.25, 0.20, 0.12, 0.08])
# Simulating Customer Acquisition Cost (CAC) based on channel
cac_map = {'Social Media': 45, 'Google Ads': 60, 'Direct Organic': 5, 'Affiliate': 30, 'Email Market': 15}
cust_cac = [cac_map[ch] for ch in cust_channels]

df_customers = pd.DataFrame({
    'CustomerID': customer_ids,
    'SignupDate': [START_DATE + timedelta(days=int(np.random.randint(0, 500))) for _ in range(NUM_CUSTOMERS)],
    'AcquisitionChannel': cust_channels,
    'CAC': cust_cac,
    'Region': np.random.choice(['North', 'South', 'East', 'West'], size=NUM_CUSTOMERS, p=[0.4, 0.2, 0.15, 0.25])
})

# 3. Generate Dim_Products
print("📦 Generating Product Dimension...")
product_ids = [f"PROD_{str(i).zfill(3)}" for i in range(1, NUM_PRODUCTS + 1)]
categories = ['Electronics', 'Apparel', 'Home & Kitchen', 'Beauty & Wellness', 'Books']
prod_cats = np.random.choice(categories, size=NUM_PRODUCTS)
base_costs = np.random.uniform(5, 150, size=NUM_PRODUCTS)
# 30% to 50% profit margin markup
selling_prices = base_costs * np.random.uniform(1.3, 1.5, size=NUM_PRODUCTS)

df_products = pd.DataFrame({
    'ProductID': product_ids,
    'Category': prod_cats,
    'COGS': np.round(base_costs, 2),
    'SellingPrice': np.round(selling_prices, 2)
})

# 4. Generate Fact_Transactions (High-Frequency Flow)
print("💳 Generating High-Frequency Transactions (This will take a few seconds)...")
tx_ids = [f"TX_{str(i).zfill(7)}" for i in range(1, NUM_TRANSACTIONS + 1)]

# Create realistic distribution for dates (incorporating high-frequency time decay)
delta_days = (END_DATE - START_DATE).days
random_days = np.random.randint(0, delta_days, size=NUM_TRANSACTIONS)
random_seconds = np.random.randint(0, 86400, size=NUM_TRANSACTIONS)

tx_dates = [START_DATE + timedelta(days=int(d), seconds=int(s)) for d, s in zip(random_days, random_seconds)]
tx_dates.sort() # Temporal ordering

# Assign transactions to customers using a Pareto-like distribution (80/20 rule: top customers buy more frequently)
cust_probs = np.random.exponential(scale=1.0, size=NUM_CUSTOMERS)
cust_probs /= cust_probs.sum()
tx_customers = np.random.choice(customer_ids, size=NUM_TRANSACTIONS, p=cust_probs)

# Assign products and quantities
tx_products = np.random.choice(product_ids, size=NUM_TRANSACTIONS)
tx_quantities = np.random.choice([1, 2, 3, 4, 5], size=NUM_TRANSACTIONS, p=[0.7, 0.18, 0.07, 0.03, 0.02])

# Add discounts (mostly 0, sometimes 10-20%)
tx_discounts = np.random.choice([0.0, 0.1, 0.2], size=NUM_TRANSACTIONS, p=[0.8, 0.15, 0.05])

df_transactions = pd.DataFrame({
    'TransactionID': tx_ids,
    'CustomerID': tx_customers,
    'ProductID': tx_products,
    'Timestamp': tx_dates,
    'Quantity': tx_quantities,
    'Discount': tx_discounts
})

# Inject Anomaly/Fraud (0.5% of transactions have massive skew to test your outliers script later)
print("⚠️ Injecting financial anomalies...")
anomaly_indices = np.random.choice(df_transactions.index, size=int(NUM_TRANSACTIONS * 0.005), replace=False)
df_transactions.loc[anomaly_indices, 'Quantity'] = np.random.randint(50, 100, size=len(anomaly_indices))

# Inject Returns/Cancellations (Status: Completed or Returned)
df_transactions['Status'] = np.random.choice(['Completed', 'Returned'], size=NUM_TRANSACTIONS, p=[0.93, 0.07])

# 5. Exporting to CSV Files
print("💾 Saving files to Data_Science_Python folder...")
df_customers.to_csv('Dim_Customers.csv', index=False)
df_products.to_csv('Dim_Products.csv', index=False)
df_transactions.to_csv('Fact_Transactions.csv', index=False)

print("✅ Step 2 Complete! 3 Premium Files Generate Ho Chuki Hain.")
print(f"Total Transactions Logged: {len(df_transactions):,}")