import csv

# Define the input and output file names
input_file = 'assignment data.csv'
output_file = 'result-data.csv'

# Initialize lists to store data
data = []

try:
    # Read the input CSV file and store the data
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Calculate the average price per square foot
    total_price_sqft = 0
    valid_data = 0

    for row in data:
        if row['price'] and float(row['sq__ft']) > 0:
            valid_data += 1
            total_price_sqft += (float(row['price']) / float(row['sq__ft']))

    average_price_per_sqft = total_price_sqft / valid_data

    # Filter properties that were sold for less than the average price per square foot
    filtered_data = [row for row in data if float(row['sq__ft']) > 0 and float(row['price']) / float(row['sq__ft']) < average_price_per_sqft]

    # Write the filtered data to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_data)

    print(f"Filtered data saved to '{output_file}'")

except Exception as e:
    print(f"An error occurred: {str(e)}")