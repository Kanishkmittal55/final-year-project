import json

# Load the extracted chemicals with synonyms from the enriched_chemicals.json file
def load_chemicals(file_path):
    try:
        with open(file_path, 'r') as f:
            chemicals = json.load(f)
        return chemicals
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading chemicals: {e}")
        return []

# Load the product details from yesstyle_product_details.txt
def load_product_details(file_path):
    products = []
    try:
        with open(file_path, 'r') as f:
            product = {}
            for line in f:
                line = line.strip()

                # Ensure line contains expected structure before splitting
                if line.startswith("Product URL:") and len(line.split("Product URL: ")) > 1:
                    product['Product URL'] = line.split("Product URL: ")[1]
                elif line.startswith("Product Name:") and len(line.split("Product Name: ")) > 1:
                    product['Product Name'] = line.split("Product Name: ")[1]
                elif line.startswith("Major Ingredients:") and len(line.split("Major Ingredients: ")) > 1:
                    product['Major Ingredients'] = line.split("Major Ingredients: ")[1]
                elif line == "=" * 50:
                    # Only append the product if it has the required keys
                    if 'Product URL' in product and 'Product Name' in product and 'Major Ingredients' in product:
                        products.append(product)
                    product = {}
    except FileNotFoundError as e:
        print(f"Error loading product details: {e}")
    return products

# Function to find exact or synonym chemical matches in product major ingredients
def find_matching_products(chemicals, products):
    matching_products = []
    
    for product in products:
        # Get the major ingredients from the product
        major_ingredients = product.get('Major Ingredients', '')
        
        matched_chemicals = []
        
        # Iterate through each chemical and its synonyms
        for chemical_data in chemicals:
            claimed_ingredient = chemical_data.get("Claimed Ingredient")
            synonyms = chemical_data.get("Synonyms", [])
            
            # Check if the claimed ingredient or any synonym is present in the major ingredients
            if claimed_ingredient in major_ingredients:
                matched_chemicals.append(claimed_ingredient)
            else:
                for synonym in synonyms:
                    if synonym in major_ingredients:
                        matched_chemicals.append(f"{claimed_ingredient} (synonym: {synonym})")
                        break  # No need to check further synonyms if one is already matched
        
        # If there are any matches, add the product to the results
        if matched_chemicals:
            matching_products.append({
                "Product URL": product.get("Product URL"),
                "Product Name": product.get("Product Name"),
                "Matched Chemicals": matched_chemicals
            })
    
    return matching_products

# Save the matching products to a file
def save_matching_products(file_path, matching_products):
    try:
        with open(file_path, 'w') as f:
            for product in matching_products:
                f.write(f"Product URL: {product['Product URL']}\n")
                f.write(f"Product Name: {product['Product Name']}\n")
                f.write(f"Matched Chemicals: {', '.join(product['Matched Chemicals'])}\n")
                f.write("=" * 50 + "\n")
        print(f"Matching products saved to {file_path}")
    except IOError as e:
        print(f"Error saving matching products: {e}")

# Main function
def main():
    # Load chemicals and products from files
    chemicals_file = '../extracted_chemicals.json'  # Updated file with synonyms
    products_file = '../yesstyle_product_details.txt'
    
    chemicals = load_chemicals(chemicals_file)
    products = load_product_details(products_file)
    
    if chemicals and products:
        # Find products with matching chemicals or synonyms
        matching_products = find_matching_products(chemicals, products)
        
        # Save the matching products to a file
        output_file = 'matching_products.txt'
        save_matching_products(output_file, matching_products)

if __name__ == "__main__":
    main()
