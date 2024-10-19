import json
from itemadapter import ItemAdapter

class JsscraperPipeline:
    def open_spider(self, spider):
        # Prepare an empty list to store items
        self.items = []

    def close_spider(self, spider):
        # Once spider finishes, write all items as a properly formatted JSON array
        with open(f'{spider.name}_output.json', 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Convert all fields to lowercase
        lowercase_item = {
            field: adapter.get(field).lower() if isinstance(adapter.get(field), str) else adapter.get(field) 
            for field in adapter.field_names()
        }
        
        # Append the processed item to the items list
        self.items.append(lowercase_item)

        return item
