import json

# Define input and output file paths
input_file = "../yesstyle_products_beauty_lips.txt"
output_file = "yesstyle_product_minimal_details.json"

# Initialize a list to hold extracted product details
products = []

# Open and process the file
with open(input_file, "r", encoding="utf-8") as file:
    current_product = {}
    for line in file:
        line = line.strip()

        # Check for the start of a new product item
        if line.startswith("product:"):
            # Convert the line to a dictionary using eval to extract all product details
            current_product = eval(line.split("product: ")[1].strip())

        elif line.startswith("url:"):
            # Extract the URL and add it to the current product's details
            product_url = line.split("url: ")[1].strip()
            if current_product:
                current_product["url"] = product_url
                products.append(current_product)  # Append the full product with url to the list
                current_product = {}  # Reset for the next product

# Save extracted product details as JSON
with open(output_file, "w", encoding="utf-8") as output:
    json.dump(products, output, indent=4)

print(f"Product details (product dictionary and url) have been extracted and saved to '{output_file}'")
