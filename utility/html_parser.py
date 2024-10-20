from bs4 import BeautifulSoup
import json

# Load the HTML file
with open("./jsScraper/yesstyle_initial_response.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Initialize an empty list to store extracted data
products_data = []

# Extract the required data (for example, product names and review count)
product_containers = soup.find_all("div", class_="productContainer")  # Assuming this is the class for product divs

for product in product_containers:
    # Extract product name
    product_name = product.find("a", class_="name").get_text(strip=True) if product.find("a", class_="name") else None
    
    # Extract review count
    review_count = product.find("span", class_="reviewCount").get_text(strip=True) if product.find("span", class_="reviewCount") else "0"
    
    # Extract other information like price, rating, etc.
    price = product.find("span", class_="price").get_text(strip=True) if product.find("span", class_="price") else None

    # Append the extracted data to the list
    products_data.append({
        "product_name": product_name,
        "review_count": review_count,
        "price": price
    })

# Save the extracted data into a JSON file
with open("yesstyle_products_data.json", "w", encoding="utf-8") as output_file:
    json.dump(products_data, output_file, ensure_ascii=False, indent=4)

print("Data extraction complete. Check 'yesstyle_products_data.json' for results.")
