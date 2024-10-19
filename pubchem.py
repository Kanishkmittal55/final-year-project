import os
import json
import pubchempy as pcp
import scrapy
import argparse

class PubchemSpider(scrapy.Spider):
    name = "pubchem"
    allowed_domains = ["pubchem.ncbi.nlm.nih.gov"]

    def __init__(self, json_file=None, *args, **kwargs):
        super(PubchemSpider, self).__init__(*args, **kwargs)
        self.json_file = json_file
        self.chemicals = []

        # Load the JSON data
        if json_file:
            with open(json_file, 'r') as file:
                self.data = json.load(file)

            # Assuming 'chemicals' key in your JSON contains chemical names
            self.chemicals = self.data.get('product_type', [])

    def start_requests(self):
        # Using PubChemPy to query each chemical in the JSON file
        for chemical in self.chemicals:
            # PubChemPy search for the chemical
            compound = pcp.get_compounds(chemical, 'name')
            for comp in compound:
                # Scrapy's way of yielding the results for storage or further processing
                yield {
                    'name': chemical,
                    'cid': comp.cid,
                    'molecular_formula': comp.molecular_formula,
                    'molecular_weight': comp.molecular_weight,
                    'iupac_name': comp.iupac_name,
                    'canonical_smiles': comp.canonical_smiles,
                    'isomeric_smiles': comp.isomeric_smiles
                }

# Function to list available JSON files in the current directory
def list_json_files(directory='.'):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

# Function to create a CLI interface using argparse
def create_cli():
    parser = argparse.ArgumentParser(description="Run Pubchem Scrapy spider with CLI for selecting JSON file.")
    parser.add_argument(
        "--dir", 
        help="Directory to look for JSON files", 
        default="."
    )
    args = parser.parse_args()

    # List available JSON files
    json_files = list_json_files(args.dir)
    
    if not json_files:
        print("No JSON files found in the directory.")
        return None

    # Prompt user to select a JSON file
    print("Available JSON files:")
    for idx, file in enumerate(json_files, start=1):
        print(f"{idx}. {file}")

    # Ask the user to select one
    selection = int(input("Select a file by number: "))
    
    if selection < 1 or selection > len(json_files):
        print("Invalid selection.")
        return None
    
    # Return the selected JSON file
    selected_file = json_files[selection - 1]
    print(f"Selected file: {selected_file}")
    return selected_file

# Main function to run the spider programmatically
def run_spider(selected_file):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # Create a Scrapy CrawlerProcess instance with project settings
    process = CrawlerProcess(get_project_settings())
    
    # Start the spider and pass the selected file as an argument
    process.crawl(PubchemSpider, json_file=selected_file)
    process.start()  # Blocking call, will run the spider

if __name__ == "__main__":
    # CLI logic
    selected_json_file = create_cli()

    if selected_json_file:
        run_spider(selected_json_file)
