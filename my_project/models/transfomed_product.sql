-- models/transformed_product_images.sql
{{ config(materialized='table') }}

WITH source_data AS (
    SELECT
        message_id as product_id,
        product_name,
        price_in_birr  -- Rename the column to be clearer
    FROM {{ source('telegram_data', 'transformed_medical_product') }}
)

SELECT   -- Ensure unique channel usernames
    product_id,
    product_name,
    price_in_birr  -- Rename the column to be clearer
FROM source_data
