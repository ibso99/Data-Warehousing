import os
import csv
import json
from dotenv import load_dotenv
from telethon import TelegramClient, types
from logger import Logger  # Import the logger class

# Load environment variables
load_dotenv()

class TelegramChannelScraper:
    """
    A class to scrape messages and media from specified Telegram channels and store them in a CSV file.

    Attributes:
    -----------
    api_id : int
        Telegram API ID for authentication.
    api_hash : str
        Telegram API Hash for authentication.
    session_name : str
        Session name for the Telegram client.
    media_dir : str
        Directory to store downloaded media files.
    csv_file : str
        Name of the CSV file to store scraped data.
    channels : list
        List of Telegram channel usernames to scrape.
    logger : ScraperLogger
        Logger for logging information during the scraping process.
    """

    def __init__(self, api_id, api_hash, session_name,  media_dir='../data/photos', 
                 csv_file='../data/telegram_data.csv', text_channels=None, image_channels=None,
                 log_file='../data/scraper.log',last_message_ids_file='../data/last_message_ids.json'):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.media_dir = media_dir
        self.csv_file = csv_file
        self.text_channels = text_channels or []
        self.image_channels = image_channels or []
        self.last_message_ids_file = last_message_ids_file
        
        # Initialize the logger with a dynamic log file path
        self.logger = Logger(log_file=log_file)

        # Create media directory
        os.makedirs(self.media_dir, exist_ok=True)
        # Load last message ids
        self.last_message_ids = self.load_last_message_ids()
    def load_last_message_ids(self):
      """Load last message ids from JSON file, if exists, returns empty dict if not"""
      try:
        with open(self.last_message_ids_file,'r') as f:
          return json.load(f)
      except (FileNotFoundError, json.JSONDecodeError):
        return {}
    def save_last_message_ids(self):
      """Save last message ids to json file"""
      with open(self.last_message_ids_file,'w') as f:
        json.dump(self.last_message_ids,f,indent=4)    

    async def scrape_channel(self, client, channel_username, writer, scrape_images=False):
        """
        Scrapes all messages from a single channel and writes to the CSV file.

        Parameters:
        ----------
        client : TelegramClient
            The authenticated Telegram client.
        channel_username : str
            The username of the channel to scrape.
        writer : csv.writer
            CSV writer object to write data to the CSV file.
            scrape_images : bool
            Flag to determine if image download is needed.
        """
        try:
            entity = await client.get_entity(channel_username)
            channel_title = entity.title  # Extract the channel's title
        except ValueError as ve:
           self.logger.error(f"Could not get entity for {channel_username}: {ve}")
           return
        except Exception as e:
           self.logger.error(f"Unexpected error getting entity for {channel_username}: {e}")
           return
        self.logger.info(f"Scraping all history from {channel_username}...")  # Log the start of scraping
        last_message_id = self.last_message_ids.get(channel_username,0) #get the last message id processed, it returns 0 if no data is available for that channel
        try:
            # Scraping all messages from the channel (set limit=None)
            async for message in client.iter_messages(entity, limit=500):
                media_path = await self.download_media(client, message, channel_username,scrape_images) if scrape_images else None
                
                # Write the data to the CSV file
                writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

            self.logger.info(f"Successfully scraped all history from {channel_username}")  # Log success message
        except Exception as e:
            self.logger.error(f"Error while scraping {channel_username}: {e}")  # Log any error
    async def download_media(self, client, message, channel_username,scrape_images):
        """
        Downloads media from the message if available.

        Parameters:
        ----------
        client : TelegramClient
            The authenticated Telegram client.
        message : telethon.tl.types.Message
            The message object containing potential media.
        channel_username : str
            The username of the channel.
        scrape_images : bool
           Flag that defines whether to download images or not

        Returns:
        -------
        str or None
            The path of the downloaded media file, or None if no media is present.
        """
        if not scrape_images:
           return None
        if message.media:
           if isinstance(message.media, types.MessageMediaPhoto):
              try:
                  file_extension = ".jpg"
                  
                  if message.media.photo.file_reference:
                      file_extension = ".jpg" if message.media.photo.file_reference else ".jpg"

                  channel_handle = channel_username.split('/')[-1]
                  
                  filename = f"{channel_handle}_{message.id}{file_extension}"
                  media_path = os.path.join(self.media_dir, filename)

                  await client.download_media(message.media, media_path)
                  self.logger.debug(f"Downloaded photo from message ID {message.id} to {media_path}")
                  return media_path
              except Exception as e:
                  self.logger.error(f"Error downloading photo from message ID {message.id}: {e}")
                  return None
           elif isinstance(message.media, types.MessageMediaDocument):
                try:
                    file_extension = ""
                    if message.media.document.mime_type == "image/png":
                        file_extension = ".png"
                    elif message.media.document.mime_type == "image/jpeg":
                         file_extension = ".jpg"
                    else:
                       return None
                    channel_handle = channel_username.split('/')[-1]
                    filename = f"{channel_handle}_{message.id}{file_extension}"
                    media_path = os.path.join(self.media_dir, filename)
                    await client.download_media(message.media, media_path)
                    self.logger.debug(f"Downloaded document from message ID {message.id} to {media_path}")
                    return media_path
                except Exception as e:
                    self.logger.error(f"Error downloading document from message ID {message.id}: {e}")
                    return None
        return None

    async def run(self):
        """
        Runs the scraping process, initializing the Telegram client and processing each channel.
        """
        self.logger.info("Starting the full history scraping process...")  # Log the start of scraping
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])

                 #Scraping text channels with not image download
                for channel in self.text_channels:
                    await self.scrape_channel(client, channel, writer, scrape_images=False)

                #Scraping images with image download option
                for channel in self.image_channels:
                    await self.scrape_channel(client, channel, writer, scrape_images=True)
        # Save the last message IDs to the file
        self.save_last_message_ids()
    def load_config(config_file='channel.json'):
        """Loads channel configuration from a JSON file."""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('text_channels', []), config.get('image_channels', [])
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.")
            return [], []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{config_file}'.")
            return [], []    
if __name__ == "__main__":
    # Get credentials from .env
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')

    # Validate API credentials
    if not api_id or not api_hash:
        raise ValueError("Your API ID or Hash cannot be empty or None. Please check your .env file.")

    # List of channels to scrape
    text_channels, image_channels = load_config()

    # Specify the log file path dynamically
    log_file_path = '../data/scraper.log'  # You can change this path as needed

    # Initialize the scraper
    scraper = TelegramChannelScraper(api_id=api_id, api_hash=api_hash, 
                                      session_name='../data/scraping_session', 
                                      text_channels=text_channels_to_scrape, image_channels=image_channels_to_scrape, log_file=log_file_path)

    # Start the scraping process
    import asyncio
    asyncio.run(scraper.run())