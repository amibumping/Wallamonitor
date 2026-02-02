  All credits go to [@danielhuici](https://github.com/danielhuici/Wallamonitor) for making Wallamonitor, I just added Docker support for amd64/arm64 platforms.

  For info on how Wallamonitor works, go to [https://github.com/danielhuici](https://github.com/danielhuici/Wallamonitor)
  
  ## Configuration 🛠️

  Docker compose example:
  ```yaml  
services:
  wallamonitor:
    image: amibumping/wallamonitor:latest
    container_name: wallamonitor
    restart: unless-stopped
    environment:
      - TZ=Europe/Madrid
      - TELEGRAM_CHANNEL_ID='-channel_id'
      - TELEGRAM_TOKEN='telegram_token'      
     
    volumes:
      - /mnt/ssd/wallamonitor/args.json:/app/args.json
```
Check out [args.json](./args.json) for an example


  ### Parameters:
  
  | Parameter                  | Description                                                                                               | Example                  | Mandatory         |
  |----------------------------|-----------------------------------------------------------------------------------------------------------|--------------------------|-------------------|
  | `search_query`             | Main search term. Only items containing this phrase in their title will be found.                         | `"laptop"`               | **Yes**          |
  | `min_price`                | Minimum item price.                                                                                       | `"100"`                  | **Yes**          |
  | `max_price`                | Maximum item price.                                                                                       | `"500"`                  | **Yes**          |
  | `latitude`                 | Latitude of your location for distance-based filtering.                                                   | `"40.4165"`              | No               |
  | `longitude`                | Longitude of your location for distance-based filtering.                                                  | `"-3.70256"`             | No               |
  | `max_distance`             | Search range (in kilometers) from the specified latitude/longitude. Use `"0"` for no limit.               | `"10"`                   | No               |
  | `condition`                | Item condition to filter by. Options: `all`, `new`, `as_good_as_new`, `good`, `fair`, `has_given_it_all`. | `"good"`                 | No               |
  | `title_exclude`            | List of words that, if present in the title, will exclude an item.                                        | `["broken", "parts"]`    | No               |
  | `description_exclude`      | List of words that, if present in the description, will exclude an item.                                  | `["damaged"]`            | No               |
  | `title_must_include`       | List of required words in the title. If none of these words appear, the item will be excluded.            | `["Intel", "i5"]`        | No               |
  | `description_must_include` | List of required words in the description. If none of these words appear, the item will be excluded.      | `["working"]`            | No               |
  | `title_first_word_include` | Notify only if the first word of the title matches the specified word.                                    | `"New"`                  | No               |


  The bot will monitor Wallapop periodically (default 15s) and send notifications to your specified Telegram channel whenever new items match your criteria.

  ---







