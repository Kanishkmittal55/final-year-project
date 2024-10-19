# Makefile for Scrapy commands

# Variables
SPIDER_NAME=bookspider
DOMAIN=books.toscrape.com
SPIDER_FOLDER=bookscraper/bookscraper/spiders  # Define the custom folder for the spider

# Create a new spider in a specified "spiders" folder
create-spider:
	@mkdir -p $(SPIDER_FOLDER)
	@scrapy genspider $(SPIDER_NAME) $(DOMAIN)
	@mv $(SPIDER_NAME).py $(SPIDER_FOLDER)

# Crawl using the default spider
crawl:
	@cd bookscraper
	@scrapy crawl $(SPIDER_NAME)

# Crawl and store the output in a JSON file
crawl-json:
	@scrapy crawl $(SPIDER_NAME) -o output.json

# Crawl and store the output in a CSV file
crawl-csv:
	@scrapy crawl $(SPIDER_NAME) -o output.csv

# List all spiders
list-spiders:
	@scrapy list

# Run Scrapy shell
shell:
	@scrapy shell $(DOMAIN)

# Clean the output files
clean:
	@rm -f output.json output.csv

# A .PHONY target prevents conflicts with file names
.PHONY: create-spider crawl crawl-json crawl-csv list-spiders shell clean
