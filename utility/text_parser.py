def extract_product_urls(file_path):
    product_urls = []

    # Open the txt file and read line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            # Check if the line starts with 'url:', indicating the product URL
            if line.startswith("url:"):
                # Extract the URL and add it to the list
                url = line.split("url: ")[1].strip()
                product_urls.append(url)

    return product_urls

# Save the product URLs to a new file (optional)
def save_product_urls(output_file, product_urls):
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in product_urls:
            file.write(f"{url}\n")

# Main function
def main():
    input_file = '../yesstyle_products.txt'  # Replace with your actual file path
    output_file = '../extracted_products.txt'  # File to save extracted URLs
    
    # Extract product URLs
    product_urls = extract_product_urls(input_file)
    
    # Save extracted URLs (optional)
    save_product_urls(output_file, product_urls)
    
    # Print the extracted URLs (for verification)
    print(f"Extracted {len(product_urls)} product URLs:")
    for url in product_urls:
        print(url)

if __name__ == "__main__":
    main()
