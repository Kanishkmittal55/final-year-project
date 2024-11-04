import psycopg2
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class JsscraperPipeline:
    def open_spider(self, spider):
        # Initialize a connection to the PostgreSQL database
        self.connection = psycopg2.connect(
            host="dpg-csiveslsvqrc73ekljr0-a.oregon-postgres.render.com",
            database="scraper_e6jv",
            user="scraper_e6jv_user",
            password="KYecsGcmpFath3iCkpolng4y8XGvZ3rE",
            port="5432"
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Convert item to ItemAdapter for easier access to fields
        adapter = ItemAdapter(item)
        
        # Validate necessary fields
        if not adapter.get('product_id') or not adapter.get('name'):
            raise DropItem(f"Missing product_id or name in {item}")
        
        # Map spider name to table name directly
        table_name = "yesstyle_beauty_cheeks"  # e.g., yesstyle_items
        
        # Define SQL query with predefined columns (assuming exact field-to-column matching)
        query = f"""
            INSERT INTO {table_name} (
                product_id, name, image_url, brand_name, brand_id, sell_price, list_price,
                discount, discount_value, color_css, url
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """
        
        # Extract values in the order they appear in the table
        values = (
            adapter.get("product_id"),
            adapter.get("name"),
            adapter.get("images"),
            adapter.get("brand_name"),
            adapter.get("brand_id"),
            adapter.get("sell_price"),
            adapter.get("list_price"),
            adapter.get("discount"),
            adapter.get("discount_value"),
            adapter.get("color_css"),
            adapter.get("url")
        )
        
        # Execute the insert query
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except psycopg2.Error as e:
            spider.logger.error(f"Database insertion error: {e}")
            self.connection.rollback()
        
        return item
