import json
import csv

# Load the extracted chemicals from the PDF (this is the JSON list of chemicals)
def load_extracted_chemicals(json_file_path):
    with open(json_file_path, 'r') as file:
        chemicals = json.load(file)
    return chemicals

# Load the website scraped data
def load_website_data(json_file_path):
    with open(json_file_path, 'r') as file:
        website_data = json.load(file)
    return website_data

# Function to search for exact chemical matches in the website data
def find_products_with_exact_chemicals(chemicals, website_data):
    matched_products = []

    for chemical in chemicals:
        for product in website_data:
            # Extract key ingredients from the website product data and convert to lowercase
            key_ingredients = product.get('key_ingredients', "").lower()
            chemical_lower = chemical.lower()

            # Check if the entire chemical name is in the key ingredients (as a whole)
            if chemical_lower in key_ingredients:
                matched_products.append({
                    'claimed_chemical': chemical,
                    'brand_name': product.get('brand_name', 'Unknown'),
                    'product_name': product.get('product_name', 'Unknown'),
                    'key_ingredients': key_ingredients,
                    'site_url': product.get('site_url', 'Unknown')
                })
                break  # Stop searching once a match is found for this product

    return matched_products

# Function to save the results to CSV
def save_to_csv(matched_products, output_file):
    # CSV header
    header = ['Claimed Ingredient', 'Brand Name', 'Product Name', 'Product URL']
    
    # Write to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for product in matched_products:
            writer.writerow({
                'Claimed Ingredient': product['claimed_chemical'],
                'Brand Name': product['brand_name'],
                'Product Name': product['product_name'],
                'Product URL': product['site_url']
            })

# Example usage
if __name__ == "__main__":
    # Path to the extracted chemicals JSON
    extracted_chemicals_file = 'extracted_chemicals.json'  # Replace with your file path

    # Path to the website data JSON
    website_data_file = './data/theordinary_output.json'  # Replace with your file path

    # Output CSV file
    output_csv_file = 'matched_chemicals_products.csv'

    # Load extracted chemicals from PDF
    chemicals = load_extracted_chemicals(extracted_chemicals_file)

    # Load website data
    website_data = load_website_data(website_data_file)

    # Find products with exact chemical matches
    matched_products = find_products_with_exact_chemicals(chemicals, website_data)

    # Output the matched products to a CSV file
    save_to_csv(matched_products, output_csv_file)

    print(f"CSV file saved as {output_csv_file}")
