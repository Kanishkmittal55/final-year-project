import sys
import os

# Add the parent directory of the project to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, send_file
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

app = Flask(__name__)
CORS(app)  

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