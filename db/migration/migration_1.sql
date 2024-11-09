CREATE TABLE yesstyle_beauty_eyes (
    id SERIAL PRIMARY KEY,
    product_id BIGINT,
    name TEXT,
    image_url TEXT,
    brand_name TEXT,
    brand_id INT,
    sell_price TEXT,
    list_price TEXT,
    discount TEXT,
    discount_value FLOAT4,
    color_css TEXT,
    url TEXT,
    ingredients TEXT,
    batch_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger function to update the updated_at column
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to set created_at and updated_at
CREATE TRIGGER set_timestamps
BEFORE INSERT OR UPDATE ON yesstyle_beauty_eyes
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
