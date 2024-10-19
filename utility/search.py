import pdfplumber
import json

# Function to extract text from a specific column in the PDF
def extract_column_from_pdf(pdf_path, column_number=1):
    column_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            
            if table:
                # Extract the specified column
                for row in table:
                    if len(row) > column_number:  # Ensure the column exists in the row
                        column_data.append(row[column_number])
    
    return column_data

# Path to your PDF file
pdf_path = "doc.pdf"

# Extract data from the specific column (change `column_number` as needed)
column_data = extract_column_from_pdf(pdf_path, column_number=1)

# Convert the extracted column data to JSON format
column_data_json = json.dumps(column_data, indent=4)

# Print the JSON formatted data
print(column_data_json)

# Optionally, save the JSON data to a file
with open('extracted_column_data.json', 'w') as json_file:
    json_file.write(column_data_json)
