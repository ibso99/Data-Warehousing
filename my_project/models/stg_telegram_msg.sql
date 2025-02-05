WITH source AS (
    SELECT *
    FROM {{ source('telegram_data', 'medical_telegram_messages') }}
)
SELECT
    id,
    channel_title,
    channel_username,
    message_id,
    message
FROM source