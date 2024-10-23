Below is a Python script to filter real estate sales data based on whether the price per square foot is less than the average:

1. It reads the data from sales-data.csv.
2. Computes the average price per square foot.
3. Filters properties that have a price per square foot below the average.
4. Writes the filtered data to a new CSV file named filtered-sales-data.csv.

#### `filter_sales.py:`

```python
import csv

# Define input and output file names
input_file = 'sales-data.csv'
output_file = 'filtered-sales-data.csv'

# Function to read CSV and calculate average price per foot
def calculate_average_price_per_foot(data):
    total_price = 0
    total_sqft = 0
    for row in data:
        price = float(row['Price'])
        sqft = float(row['Square Footage'])
        total_price += price
        total_sqft += sqft
    
    if total_sqft == 0:
        return 0
    
    return total_price / total_sqft

# Read CSV data
with open(input_file, mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

    # Calculate average price per square foot
    avg_price_per_foot = calculate_average_price_per_foot(data)

    # Filter properties with price per foot less than average
    filtered_data = [
        row for row in data if float(row['Price']) / float(row['Square Footage']) < avg_price_per_foot
    ]

# Write filtered data to a new CSV file
with open(output_file, mode='w', newline='') as csvfile:
    fieldnames = data[0].keys()  # Assuming all rows have the same keys
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(filtered_data)

print(f"Filtered data saved to {output_file}")
```
# How to Run the Script
1. Make sure you have Python 3 installed on your system.
2. Save the script as `filter_sales.py` and place `sales-data.csv` in the same directory.
3. Run the script using:

```bash
python filter_sales.py
```