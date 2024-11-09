import sys
import os

# Add the parent directory of the project to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, send_file
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from jsScraper.spiders.sephora import SephoraSpider
import threading
import os
import json
from flask_cors import CORS
from itemadapter import ItemAdapter
import shutil
import logging
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)  

# Database connection details
connection = psycopg2.connect(
    host="dpg-csiveslsvqrc73ekljr0-a.oregon-postgres.render.com",
    database="scraper_e6jv",
    user="scraper_e6jv_user",
    password="KYecsGcmpFath3iCkpolng4y8XGvZ3rE",
    port="5432"
)

# Helper function to query by category
def fetch_data_by_category(category):
    try:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        logging.error(f"Error fetching data for category {category}: {str(e)}")
        return {"error": str(e)}, 500

# Dynamic endpoints for each category
@app.route('/yesstyle/<category>', methods=['GET'])
def get_category_data(category):
    data = fetch_data_by_category(category)
    return jsonify(data)



scraped_items = []
json_file_path = None  

def collect_items(item, response, spider):
    adapter = ItemAdapter(item)
    scraped_items.append(adapter.asdict())

@defer.inlineCallbacks
def run_spider(spider_class):
    global json_file_path
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    scraped_items.clear()

    dispatcher.connect(collect_items, signal=signals.item_scraped)

    yield runner.crawl(spider_class)

    json_file_path = f'{spider_class.name}_output.json'
    print(f"json_file_path is set to: {json_file_path}")

    with open(json_file_path, 'w') as f:
        json.dump(scraped_items, f)

    # Make a local copy
    local_copy_path = f'/Users/kanishkmittal/Desktop/Dissertation/webscraper/data/{spider_class.name}_output_copy.json'
    shutil.copy(json_file_path, local_copy_path)
    logging.info(f"Local copy created at: {local_copy_path}")

    print("Stopping Twisted reactor...")
    reactor.stop()
    print("Reactor stopped.")

def start_reactor():
    print("Starting Twisted reactor...")  
    reactor.run(installSignalHandlers=False)
    print("Reactor started.")


@app.route('/scrape/sephora', methods=['GET'])
def scrape_sephora():
    global scraped_items


    if not reactor.running:
        threading.Thread(target=start_reactor).start()


    reactor.callFromThread(run_spider, SephoraSpider)


    def wait_for_spider():
        while json_file_path is None:
            pass 

    wait_for_spider()


    return jsonify({
        "message": "Scraping completed",
        "download_link": f"http://localhost:5000/download/json"
    })


@app.route('/scrape/proya', methods=['GET'])
def scrape_proya():
    global scraped_items

    if not reactor.running:
        threading.Thread(target=start_reactor).start()

    reactor.callFromThread(run_spider, ProyaSpider)
    
    def wait_for_spider():
        while json_file_path is None:
            pass

    wait_for_spider()

    return jsonify({
        "message": "Scraping completed",
        "download_link": f"http://localhost:5000/download/json"
    })


@app.route('/scrape/theordinary', methods=['GET'])
def scrape_theordinary():
    global scraped_items

    if not reactor.running:
        threading.Thread(target=start_reactor).start()

    reactor.callFromThread(run_spider, TheordinarySpider)
    
    def wait_for_spider():
        while json_file_path is None:
            pass

    wait_for_spider()

    return jsonify({
        "message": "Scraping completed",
        "download_link": f"http://localhost:5000/download/json"
    })

# # New Endpoint: Fetch data from products table where category is 'beauty-eyes'
# @app.route('/yesstyle/beauty_eyes', methods=['GET'])
# def get_yesstyle_beauty_eyes_data():
#     try:
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM products WHERE category = %s", ('beauty-eyes',))
#         rows = cursor.fetchall()
#         data = [dict(row) for row in rows]
#         return jsonify(data)
#     except Exception as e:
#         logging.error(f"Error fetching YesStyle data: {str(e)}")
#         return jsonify({"error": str(e)}), 500
    
# # New Endpoint: Fetch data from products table where category is 'beauty-cheeks'
# @app.route('/yesstyle/beauty_cheeks', methods=['GET'])
# def get_yesstyle_beauty_cheeks_data():
#     try:
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM products WHERE category = %s", ('beauty-cheeks',))
#         rows = cursor.fetchall()
#         data = [dict(row) for row in rows]
#         return jsonify(data)
#     except Exception as e:
#         logging.error(f"Error fetching YesStyle data: {str(e)}")
#         return jsonify({"error": str(e)}), 500
    
# # New Endpoint: Fetch data from products table where category is 'beauty-lips'
# @app.route('/yesstyle/beauty_lips', methods=['GET'])
# def get_yesstyle_beauty_lips_data():
#     try:
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM products WHERE category = %s", ('beauty-lips',))
#         rows = cursor.fetchall()
#         data = [dict(row) for row in rows]
#         return jsonify(data)
#     except Exception as e:
#         logging.error(f"Error fetching YesStyle data: {str(e)}")
#         return jsonify({"error": str(e)}), 500
    
# # New Endpoint: Fetch data from products table where category is 'beauty-face'
# @app.route('/yesstyle/beauty_face', methods=['GET'])
# def get_yesstyle_beauty_face_data():
#     try:
#         cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM products WHERE category = %s", ('beauty-face',))
#         rows = cursor.fetchall()
#         data = [dict(row) for row in rows]
#         return jsonify(data)
#     except Exception as e:
#         logging.error(f"Error fetching YesStyle data: {str(e)}")
#         return jsonify({"error": str(e)}), 500
    



# New Endpoint: Run a custom SQL query on the database
@app.route('/run-query', methods=['POST'])
def run_query():
    query = request.json.get('query')
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if cursor.description:  # If it's a SELECT query
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return jsonify(result)
        else:
            connection.commit()  # For INSERT, UPDATE, DELETE queries
            return jsonify({"message": "Query executed successfully"})
    except Exception as e:
        logging.error(f"Error running query: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/download/json', methods=['GET'])
def download_json():
    local_copy_path = '/Users/kanishkmittal/Desktop/Dissertation/webscraper/data/sephora_output_copy.json'  

    logging.info(f"Attempting to download file from path: {local_copy_path}")

    if os.path.exists(local_copy_path):
        try:
            return send_file(local_copy_path, as_attachment=True)
        except Exception as e:
            logging.error(f"Error sending file: {str(e)}")
            return jsonify({"error": f"Failed to send file: {str(e)}"}), 500
    else:
        logging.warning("File not found or json_file_path is None")
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(port=5000)