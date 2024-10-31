import json
from collections import Counter

# Define the input and output file paths
input_file = "yesstyle_beauty_lips.json"
output_file = "yesstyle_statistics_beauty_lips.txt"

# Load the JSON data
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Initialize a Counter to count products per brand
brand_counter = Counter()

# Count occurrences of each brand
for product in data:
    brand_name = product.get("brandName", "Unknown Brand")
    brand_counter[brand_name] += 1

# Calculate the number of unique brands and total products
unique_brands = len(brand_counter)
total_products = sum(brand_counter.values())

# Write statistics to output file
with open(output_file, "w", encoding="utf-8") as output:
    output.write(f"Total number of products: {total_products}\n")
    output.write(f"Total unique brands: {unique_brands}\n\n")
    output.write("Number of products per brand:\n")
    for brand, count in brand_counter.items():
        output.write(f"{brand}: {count}\n")

print(f"Statistics have been saved to '{output_file}'")
